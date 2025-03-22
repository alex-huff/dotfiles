#!/bin/python3

import asyncio
import datetime
import json
import math
import os
import re
import shutil
import signal
import struct
import sys
import time
from copy import deepcopy
from enum import IntEnum, auto
from xml.etree import ElementTree

import wcwidth
from dbus_next._private.util import replace_fds_with_idx, replace_idx_with_fds
from dbus_next.aio import MessageBus
from dbus_next.introspection import Interface, Node
from dbus_next.message import Message, MessageFlag
from dbus_next.proxy_object import BaseProxyInterface


class BarEvent:
    def __init__(self, event_type, payload):
        self.event_type = event_type
        self.payload = payload


class BarEventType(IntEnum):
    INITIALIZE_MEDIA_PLAYER = auto()
    UPDATE_MEDIA_PLAYER_STATE = auto()
    SHUTDOWN_MEDIA_PLAYER = auto()

    WORKSPACES_UPDATE = auto()

    CLOCK_UPDATE = auto()

    RESIZE = auto()

    def is_media_player_event(self):
        return (
            BarEventType.INITIALIZE_MEDIA_PLAYER
            <= self
            <= BarEventType.SHUTDOWN_MEDIA_PLAYER
        )


class MediaPlayerState:
    def __init__(self, media_player_dbus_name, properties, task_group, bar_event_queue):
        self.media_player_dbus_name = media_player_dbus_name
        self.task_group = task_group
        self.bar_event_queue = bar_event_queue
        self.loop = asyncio.get_running_loop()
        self.playback_status = properties["PlaybackStatus"].value
        self.loop_status = (
            properties["LoopStatus"].value if "LoopStatus" in properties else "None"
        )
        self.rate = properties["Rate"].value if "Rate" in properties else 1.0
        self.set_metadata(properties["Metadata"].value)
        self.seek(properties["Position"].value)
        self.loop_time_started_playing_from_last_known_position = None
        self.clock_task = None
        if self.is_playing():
            self.restart_clock()
        self.send_update(BarEventType.INITIALIZE_MEDIA_PLAYER)

    def set_metadata(self, metadata):
        if not metadata:
            self.track_id = self.track_artist = self.track_title = None
            self.track_length = self.track_length_seconds = math.inf
            return
        self.track_id, self.track_length, self.track_artist, self.track_title = (
            metadata[key].value if key in metadata else None
            for key in ("mpris:trackid", "mpris:length", "xesam:artist", "xesam:title")
        )
        if self.track_length is None or self.track_length < 0:
            self.track_length = self.track_length_seconds = math.inf
            return
        self.track_length = self.track_length
        self.track_length_seconds = self.track_length // 1_000_000

    def get_visible_metadata(self):
        return (self.track_length_seconds, self.track_artist, self.track_title)

    def is_playing(self):
        return self.playback_status == "Playing"

    def is_paused(self):
        return self.playback_status == "Paused"

    def is_stopped(self):
        return self.playback_status == "Stopped"

    def seek(self, new_position):
        self.last_known_position = min(self.track_length, round(max(0, new_position)))
        self.track_hit_end = self.last_known_position == self.track_length
        self.track_current_second = self.last_known_position // 1_000_000

    def update_last_known_position_to_estimated_track_current_position(self):
        self.seek(self.get_estimated_track_current_position())

    def get_estimated_track_current_position(self):
        if not self.is_playing() or self.track_hit_end:
            return self.last_known_position
        elapsed_time = (
            self.loop.time() - self.loop_time_started_playing_from_last_known_position
        )
        return self.last_known_position + elapsed_time * self.rate * 1_000_000

    def restart_clock(self):
        self.cancel_clock()
        self.loop_time_started_playing_from_last_known_position = self.loop.time()
        if self.track_hit_end:
            return
        self.clock_task = self.task_group.create_task(
            self.run_clock_till_end_of_track()
        )

    def cancel_clock(self):
        if self.clock_task is not None:
            self.clock_task.cancel()
            self.clock_task = None

    async def run_clock_till_end_of_track(self):
        while self.track_current_second < self.track_length_seconds:
            estimated_track_current_position_micros = (
                self.get_estimated_track_current_position()
            )
            estimated_track_current_position_second = int(
                estimated_track_current_position_micros // 1_000_000
            )
            next_second_to_display = max(
                self.track_current_second + 1,
                estimated_track_current_position_second + 1,
            )
            track_current_second_is_more_than_one_second_behind = (
                self.track_current_second < next_second_to_display - 1
            )
            if track_current_second_is_more_than_one_second_behind:
                # this could theoretically happen if the event loop was blocked
                # for a long time
                self.track_current_second = min(
                    self.track_length_seconds, next_second_to_display - 1
                )
                self.send_update()
                if self.track_current_second == self.track_length_seconds:
                    break
            next_second_to_display_micros = next_second_to_display * 1_000_000
            time_till_next_second_to_display_seconds = (
                next_second_to_display_micros - estimated_track_current_position_micros
            ) / (1_000_000 * self.rate)
            if time_till_next_second_to_display_seconds > 0:
                await asyncio.sleep(time_till_next_second_to_display_seconds)
            self.track_current_second += 1
            self.send_update()
        time_till_track_end_seconds = (
            self.track_length - self.get_estimated_track_current_position()
        ) / 1_000_000
        if time_till_track_end_seconds > 0:
            await asyncio.sleep(time_till_track_end_seconds / self.rate)
        self.track_hit_end = True
        self.last_known_position = self.track_length

    def send_update(self, event_type=BarEventType.UPDATE_MEDIA_PLAYER_STATE):
        payload = {
            "dbus_name": self.media_player_dbus_name,
            "playback_status": self.playback_status,
            "loop_status": self.loop_status,
            "track_artist": self.track_artist,
            "track_title": self.track_title,
            "track_current_second": self.track_current_second,
            "track_length_seconds": self.track_length_seconds,
        }
        event = BarEvent(event_type, payload)
        self.bar_event_queue.put_nowait(event)

    def shutdown(self):
        self.cancel_clock()
        self.send_update(BarEventType.SHUTDOWN_MEDIA_PLAYER)


async def watch_all_media_players_forever(task_group, bar_event_queue):
    MEDIA_PLAYER_BUS_NAME_REGEX = re.compile(r"org\.mpris\.MediaPlayer2\.(.*)")
    DBUS_BUS_NAME = "org.freedesktop.DBus"
    DBUS_OBJECT_PATH = "/org/freedesktop/DBus"
    DBUS_INTERFACE = "org.freedesktop.DBus"

    # taken from: https://gitlab.freedesktop.org/mpris/mpris-spec
    MEDIA_PLAYER_PLAYER_INTERFACE_INTROSPECTION_XML = ElementTree.fromstring(
        """\
<?xml version="1.0" ?>
<node name="/Player_Interface" xmlns:tp="http://telepathy.freedesktop.org/wiki/DbusSpec#extensions-v0">
  <interface name="org.mpris.MediaPlayer2.Player">

    <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
      <p>
        This interface implements the methods for querying and providing basic
        control over what is currently playing.
      </p>
    </tp:docstring>

    <tp:enum name="Playback_Status" tp:name-for-bindings="Playback_Status" type="s">
      <tp:enumvalue suffix="Playing" value="Playing">
        <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
          <p>A track is currently playing.</p>
        </tp:docstring>
      </tp:enumvalue>
      <tp:enumvalue suffix="Paused" value="Paused">
        <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
          <p>A track is currently paused.</p>
        </tp:docstring>
      </tp:enumvalue>
      <tp:enumvalue suffix="Stopped" value="Stopped">
        <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
          <p>There is no track currently playing.</p>
        </tp:docstring>
      </tp:enumvalue>
      <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
        <p>A playback state.</p>
      </tp:docstring>
    </tp:enum>

    <tp:enum name="Loop_Status" tp:name-for-bindings="Loop_Status" type="s">
      <tp:enumvalue suffix="None" value="None">
        <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
          <p>The playback will stop when there are no more tracks to play</p>
        </tp:docstring>
      </tp:enumvalue>
      <tp:enumvalue suffix="Track" value="Track">
        <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
          <p>The current track will start again from the begining once it has finished playing</p>
        </tp:docstring>
      </tp:enumvalue>
      <tp:enumvalue suffix="Playlist" value="Playlist">
        <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
          <p>The playback loops through a list of tracks</p>
        </tp:docstring>
      </tp:enumvalue>
      <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
        <p>A repeat / loop status</p>
      </tp:docstring>
    </tp:enum>

    <tp:simple-type name="Track_Id" type="o" array-name="Track_Id_List">
      <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
        <p>Unique track identifier.</p>
        <p>
          If the media player implements the TrackList interface and allows
          the same track to appear multiple times in the tracklist,
          this must be unique within the scope of the tracklist.
        </p>
        <p>
          Note that this should be a valid D-Bus object id, although clients
          should not assume that any object is actually exported with any
          interfaces at that path.
        </p>
        <p>
          Media players may not use any paths starting with
          <literal>/org/mpris</literal> unless explicitly allowed by this specification.
          Such paths are intended to have special meaning, such as
          <literal>/org/mpris/MediaPlayer2/TrackList/NoTrack</literal>
          to indicate "no track".
        </p>
        <tp:rationale>
          <p>
            This is a D-Bus object id as that is the definitive way to have
            unique identifiers on D-Bus.  It also allows for future optional
            expansions to the specification where tracks are exported to D-Bus
            with an interface similar to org.gnome.UPnP.MediaItem2.
          </p>
        </tp:rationale>
      </tp:docstring>
    </tp:simple-type>

    <tp:simple-type name="Playback_Rate" type="d">
      <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
        <p>A playback rate</p>
        <p>
          This is a multiplier, so a value of 0.5 indicates that playback is
          happening at half speed, while 1.5 means that 1.5 seconds of "track time"
          is consumed every second.
        </p>
      </tp:docstring>
    </tp:simple-type>

    <tp:simple-type name="Volume" type="d">
      <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
        <p>Audio volume level</p>
        <ul>
          <li>0.0 means mute.</li>
          <li>1.0 is a sensible maximum volume level (ex: 0dB).</li>
        </ul>
        <p>
          Note that the volume may be higher than 1.0, although generally
          clients should not attempt to set it above 1.0.
        </p>
      </tp:docstring>
    </tp:simple-type>

    <tp:simple-type name="Time_In_Us" type="x">
      <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
        <p>Time in microseconds.</p>
      </tp:docstring>
    </tp:simple-type>

    <method name="Next" tp:name-for-bindings="Next">
      <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
        <p>Skips to the next track in the tracklist.</p>
        <p>
          If there is no next track (and endless playback and track
          repeat are both off), stop playback.
        </p>
        <p>If playback is paused or stopped, it remains that way.</p>
        <p>
          If <tp:member-ref>CanGoNext</tp:member-ref> is
          <strong>false</strong>, attempting to call this method should have
          no effect.
        </p>
      </tp:docstring>
    </method>

    <method name="Previous" tp:name-for-bindings="Previous">
      <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
        <p>Skips to the previous track in the tracklist.</p>
        <p>
          If there is no previous track (and endless playback and track
          repeat are both off), stop playback.
        </p>
        <p>If playback is paused or stopped, it remains that way.</p>
        <p>
          If <tp:member-ref>CanGoPrevious</tp:member-ref> is
          <strong>false</strong>, attempting to call this method should have
          no effect.
        </p>
      </tp:docstring>
    </method>

    <method name="Pause" tp:name-for-bindings="Pause">
      <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
        <p>Pauses playback.</p>
        <p>If playback is already paused, this has no effect.</p>
        <p>
          Calling Play after this should cause playback to start again
          from the same position.
        </p>
        <p>
          If <tp:member-ref>CanPause</tp:member-ref> is
          <strong>false</strong>, attempting to call this method should have
          no effect.
        </p>
      </tp:docstring>
    </method>

    <method name="PlayPause" tp:name-for-bindings="PlayPause">
      <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
        <p>Pauses playback.</p>
        <p>If playback is already paused, resumes playback.</p>
        <p>If playback is stopped, starts playback.</p>
        <p>
          If <tp:member-ref>CanPause</tp:member-ref> is
          <strong>false</strong>, attempting to call this method should have
          no effect and raise an error.
        </p>
      </tp:docstring>
    </method>

    <method name="Stop" tp:name-for-bindings="Stop">
      <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
        <p>Stops playback.</p>
        <p>If playback is already stopped, this has no effect.</p>
        <p>
          Calling Play after this should cause playback to
          start again from the beginning of the track.
        </p>
        <p>
          If <tp:member-ref>CanControl</tp:member-ref> is
          <strong>false</strong>, attempting to call this method should have
          no effect and raise an error.
        </p>
      </tp:docstring>
    </method>

    <method name="Play" tp:name-for-bindings="Play">
      <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
        <p>Starts or resumes playback.</p>
        <p>If already playing, this has no effect.</p>
        <p>If paused, playback resumes from the current position.</p>
        <p>If there is no track to play, this has no effect.</p>
        <p>
          If <tp:member-ref>CanPlay</tp:member-ref> is
          <strong>false</strong>, attempting to call this method should have
          no effect.
        </p>
      </tp:docstring>
    </method>

    <method name="Seek" tp:name-for-bindings="Seek">
      <arg direction="in" type="x" name="Offset" tp:type="Time_In_Us">
        <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
          <p>The number of microseconds to seek forward.</p>
        </tp:docstring>
      </arg>
      <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
        <p>
          Seeks forward in the current track by the specified number
          of microseconds.
        </p>
        <p>
          A negative value seeks back. If this would mean seeking
          back further than the start of the track, the position
          is set to 0.
        </p>
        <p>
          If the value passed in would mean seeking beyond the end
          of the track, acts like a call to Next.
        </p>
        <p>
          If the <tp:member-ref>CanSeek</tp:member-ref> property is false,
          this has no effect.
        </p>
      </tp:docstring>
    </method>

    <method name="SetPosition" tp:name-for-bindings="Set_Position">
      <arg direction="in" type="o" tp:type="Track_Id" name="TrackId">
        <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
          <p>The currently playing track's identifier.</p>
          <p>
            If this does not match the id of the currently-playing track,
            the call is ignored as "stale".
          </p>
          <p>
            <literal>/org/mpris/MediaPlayer2/TrackList/NoTrack</literal>
            is <em>not</em> a valid value for this argument.
          </p>
        </tp:docstring>
      </arg>
      <arg direction="in" type="x" tp:type="Time_In_Us" name="Position">
        <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
          <p>Track position in microseconds.</p>
          <p>This must be between 0 and &lt;track_length&gt;.</p>
        </tp:docstring>
      </arg>
      <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
        <p>Sets the current track position in microseconds.</p>
        <p>If the Position argument is less than 0, do nothing.</p>
        <p>
          If the Position argument is greater than the track length,
          do nothing.
        </p>
        <p>
          If the <tp:member-ref>CanSeek</tp:member-ref> property is false,
          this has no effect.
        </p>
        <tp:rationale>
          <p>
            The reason for having this method, rather than making
            <tp:member-ref>Position</tp:member-ref> writable, is to include
            the TrackId argument to avoid race conditions where a client tries
            to seek to a position when the track has already changed.
          </p>
        </tp:rationale>
      </tp:docstring>
    </method>

    <method name="OpenUri" tp:name-for-bindings="Open_Uri">
      <arg direction="in" type="s" tp:type="Uri" name="Uri">
        <tp:docstring>
          <p>
            Uri of the track to load. Its uri scheme should be an element of the
            <literal>org.mpris.MediaPlayer2.SupportedUriSchemes</literal>
            property and the mime-type should match one of the elements of the
            <literal>org.mpris.MediaPlayer2.SupportedMimeTypes</literal>.
          </p>
        </tp:docstring>
      </arg>
      <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
        <p>Opens the Uri given as an argument</p>
        <p>If the playback is stopped, starts playing</p>
        <p>
          If the uri scheme or the mime-type of the uri to open is not supported,
          this method does nothing and may raise an error.  In particular, if the
          list of available uri schemes is empty, this method may not be
          implemented.
        </p>
        <p>Clients should not assume that the Uri has been opened as soon as this
           method returns. They should wait until the mpris:trackid field in the
           <tp:member-ref>Metadata</tp:member-ref> property changes.
        </p>
        <p>
          If the media player implements the TrackList interface, then the
          opened track should be made part of the tracklist, the
          <literal>org.mpris.MediaPlayer2.TrackList.TrackAdded</literal> or
          <literal>org.mpris.MediaPlayer2.TrackList.TrackListReplaced</literal>
          signal should be fired, as well as the
          <literal>org.freedesktop.DBus.Properties.PropertiesChanged</literal>
          signal on the tracklist interface.
        </p>
      </tp:docstring>
    </method>

    <property name="PlaybackStatus" tp:name-for-bindings="Playback_Status" type="s" tp:type="Playback_Status" access="read">
      <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="true"/>
      <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
        <p>The current playback status.</p>
        <p>
          May be "Playing", "Paused" or "Stopped".
        </p>
      </tp:docstring>
    </property>

    <property name="LoopStatus" type="s" access="readwrite"
              tp:name-for-bindings="Loop_Status" tp:type="Loop_Status">
      <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="true"/>
      <annotation name="org.mpris.MediaPlayer2.property.optional" value="true"/>
      <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
        <p>The current loop / repeat status</p>
        <p>May be:
          <ul>
            <li>"None" if the playback will stop when there are no more tracks to play</li>
            <li>"Track" if the current track will start again from the begining once it has finished playing</li>
            <li>"Playlist" if the playback loops through a list of tracks</li>
          </ul>
        </p>
        <p>
          If <tp:member-ref>CanControl</tp:member-ref> is
          <strong>false</strong>, attempting to set this property should have
          no effect and raise an error.
        </p>
      </tp:docstring>
    </property>

    <property name="Rate" tp:name-for-bindings="Rate" type="d" tp:type="Playback_Rate" access="readwrite">
      <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="true"/>
      <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
        <p>The current playback rate.</p>
        <p>
          The value must fall in the range described by
          <tp:member-ref>MinimumRate</tp:member-ref> and
          <tp:member-ref>MaximumRate</tp:member-ref>, and must not be 0.0.  If
          playback is paused, the <tp:member-ref>PlaybackStatus</tp:member-ref>
          property should be used to indicate this.  A value of 0.0 should not
          be set by the client.  If it is, the media player should act as
          though <tp:member-ref>Pause</tp:member-ref> was called.
        </p>
        <p>
          If the media player has no ability to play at speeds other than the
          normal playback rate, this must still be implemented, and must
          return 1.0.  The <tp:member-ref>MinimumRate</tp:member-ref> and
          <tp:member-ref>MaximumRate</tp:member-ref> properties must also be
          set to 1.0.
        </p>
        <p>
          Not all values may be accepted by the media player.  It is left to
          media player implementations to decide how to deal with values they
          cannot use; they may either ignore them or pick a "best fit" value.
          Clients are recommended to only use sensible fractions or multiples
          of 1 (eg: 0.5, 0.25, 1.5, 2.0, etc).
        </p>
        <tp:rationale>
          <p>
            This allows clients to display (reasonably) accurate progress bars
            without having to regularly query the media player for the current
            position.
          </p>
        </tp:rationale>
      </tp:docstring>
    </property>

    <property name="Shuffle" tp:name-for-bindings="Shuffle" type="b" access="readwrite">
      <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="true"/>
      <annotation name="org.mpris.MediaPlayer2.property.optional" value="true"/>
      <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
        <p>
          A value of <strong>false</strong> indicates that playback is
          progressing linearly through a playlist, while <strong>true</strong>
          means playback is progressing through a playlist in some other order.
        </p>
        <p>
          If <tp:member-ref>CanControl</tp:member-ref> is
          <strong>false</strong>, attempting to set this property should have
          no effect and raise an error.
        </p>
      </tp:docstring>
    </property>

    <property name="Metadata" tp:name-for-bindings="Metadata" type="a{sv}" tp:type="Metadata_Map" access="read">
      <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="true"/>
      <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
        <p>The metadata of the current element.</p>
        <p>
          If there is a current track, this must have a "mpris:trackid" entry
          (of D-Bus type "o") at the very least, which contains a D-Bus path that
          uniquely identifies this track.
        </p>
        <p>
          See the type documentation for more details.
        </p>
      </tp:docstring>
    </property>

    <property name="Volume" type="d" tp:type="Volume" tp:name-for-bindings="Volume" access="readwrite">
      <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="true" />
      <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
        <p>The volume level.</p>
        <p>
          When setting, if a negative value is passed, the volume
          should be set to 0.0.
        </p>
        <p>
          If <tp:member-ref>CanControl</tp:member-ref> is
          <strong>false</strong>, attempting to set this property should have
          no effect and raise an error.
        </p>
      </tp:docstring>
    </property>

    <property name="Position" type="x" tp:type="Time_In_Us" tp:name-for-bindings="Position" access="read">
        <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="false"/>
        <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
          <p>
            The current track position in microseconds, between 0 and
            the 'mpris:length' metadata entry (see Metadata).
          </p>
          <p>
            Note: If the media player allows it, the current playback position
            can be changed either the SetPosition method or the Seek method on
            this interface.  If this is not the case, the
            <tp:member-ref>CanSeek</tp:member-ref> property is false, and
            setting this property has no effect and can raise an error.
          </p>
          <p>
            If the playback progresses in a way that is inconstistant with the
            <tp:member-ref>Rate</tp:member-ref> property, the
            <tp:member-ref>Seeked</tp:member-ref> signal is emited.
          </p>
        </tp:docstring>
    </property>

    <property name="MinimumRate" tp:name-for-bindings="Minimum_Rate" type="d" tp:type="Playback_Rate" access="read">
      <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="true"/>
      <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
        <p>
          The minimum value which the <tp:member-ref>Rate</tp:member-ref>
          property can take.
          Clients should not attempt to set the
          <tp:member-ref>Rate</tp:member-ref> property below this value.
        </p>
        <p>
          Note that even if this value is 0.0 or negative, clients should
          not attempt to set the <tp:member-ref>Rate</tp:member-ref> property
          to 0.0.
        </p>
        <p>This value should always be 1.0 or less.</p>
      </tp:docstring>
    </property>

    <property name="MaximumRate" tp:name-for-bindings="Maximum_Rate" type="d" tp:type="Playback_Rate" access="read">
      <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="true"/>
      <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
        <p>
          The maximum value which the <tp:member-ref>Rate</tp:member-ref>
          property can take.
          Clients should not attempt to set the
          <tp:member-ref>Rate</tp:member-ref> property above this value.
        </p>
        <p>
          This value should always be 1.0 or greater.
        </p>
      </tp:docstring>
    </property>

    <property name="CanGoNext" tp:name-for-bindings="Can_Go_Next" type="b" access="read">
      <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="true"/>
      <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
        <p>
          Whether the client can call the <tp:member-ref>Next</tp:member-ref>
          method on this interface and expect the current track to change.
        </p>
        <p>
          If it is unknown whether a call to <tp:member-ref>Next</tp:member-ref> will
          be successful (for example, when streaming tracks), this property should
          be set to <strong>true</strong>.
        </p>
        <p>
          If <tp:member-ref>CanControl</tp:member-ref> is
          <strong>false</strong>, this property should also be
          <strong>false</strong>.
        </p>
        <tp:rationale>
          <p>
            Even when playback can generally be controlled, there may not
            always be a next track to move to.
          </p>
        </tp:rationale>
      </tp:docstring>
    </property>

    <property name="CanGoPrevious" tp:name-for-bindings="Can_Go_Previous" type="b" access="read">
      <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="true"/>
      <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
        <p>
          Whether the client can call the
          <tp:member-ref>Previous</tp:member-ref> method on this interface and
          expect the current track to change.
        </p>
        <p>
          If it is unknown whether a call to <tp:member-ref>Previous</tp:member-ref>
          will be successful (for example, when streaming tracks), this property
          should be set to <strong>true</strong>.
        </p>
        <p>
          If <tp:member-ref>CanControl</tp:member-ref> is
          <strong>false</strong>, this property should also be
          <strong>false</strong>.
        </p>
        <tp:rationale>
          <p>
            Even when playback can generally be controlled, there may not
            always be a next previous to move to.
          </p>
        </tp:rationale>

      </tp:docstring>
    </property>

    <property name="CanPlay" tp:name-for-bindings="Can_Play" type="b" access="read">
      <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="true"/>
      <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
        <p>Whether playback can be started using
           <tp:member-ref>Play</tp:member-ref> or
           <tp:member-ref>PlayPause</tp:member-ref>.
        </p>
        <p>
          Note that this is related to whether there is a "current track": the
          value should not depend on whether the track is currently paused or
          playing.  In fact, if a track is currently playing (and
          <tp:member-ref>CanControl</tp:member-ref> is <strong>true</strong>),
          this should be <strong>true</strong>.
        </p>
        <p>
          If <tp:member-ref>CanControl</tp:member-ref> is
          <strong>false</strong>, this property should also be
          <strong>false</strong>.
        </p>
        <tp:rationale>
          <p>
            Even when playback can generally be controlled, it may not be
            possible to enter a "playing" state, for example if there is no
            "current track".
          </p>
        </tp:rationale>
      </tp:docstring>
    </property>

    <property name="CanPause" tp:name-for-bindings="Can_Pause" type="b" access="read">
      <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="true"/>
      <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
        <p>Whether playback can be paused using
           <tp:member-ref>Pause</tp:member-ref> or
           <tp:member-ref>PlayPause</tp:member-ref>.
        </p>
        <p>
          Note that this is an intrinsic property of the current track: its
          value should not depend on whether the track is currently paused or
          playing.  In fact, if playback is currently paused (and
          <tp:member-ref>CanControl</tp:member-ref> is <strong>true</strong>),
          this should be <strong>true</strong>.
        </p>
        <p>
          If <tp:member-ref>CanControl</tp:member-ref> is
          <strong>false</strong>, this property should also be
          <strong>false</strong>.
        </p>
        <tp:rationale>
          <p>
            Not all media is pausable: it may not be possible to pause some
            streamed media, for example.
          </p>
        </tp:rationale>
      </tp:docstring>
    </property>

    <property name="CanSeek" tp:name-for-bindings="Can_Seek" type="b" access="read">
      <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="true"/>
      <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
        <p>
          Whether the client can control the playback position using
          <tp:member-ref>Seek</tp:member-ref> and
          <tp:member-ref>SetPosition</tp:member-ref>.  This may be different for
          different tracks.
        </p>
        <p>
          If <tp:member-ref>CanControl</tp:member-ref> is
          <strong>false</strong>, this property should also be
          <strong>false</strong>.
        </p>
        <tp:rationale>
          <p>
            Not all media is seekable: it may not be possible to seek when
            playing some streamed media, for example.
          </p>
        </tp:rationale>
      </tp:docstring>
    </property>

    <property name="CanControl" tp:name-for-bindings="Can_Control" type="b" access="read">
      <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="false"/>
      <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
        <p>Whether the media player may be controlled over this interface.</p>
        <p>
          This property is not expected to change, as it describes an intrinsic
          capability of the implementation.
        </p>
        <p>
          If this is <strong>false</strong>, clients should assume that all
          properties on this interface are read-only (and will raise errors
          if writing to them is attempted), no methods are implemented
          and all other properties starting with "Can" are also
          <strong>false</strong>.
        </p>
        <tp:rationale>
          <p>
            This allows clients to determine whether to present and enable
            controls to the user in advance of attempting to call methods
            and write to properties.
          </p>
        </tp:rationale>
      </tp:docstring>
    </property>

    <signal name="Seeked" tp:name-for-bindings="Seeked">
      <arg name="Position" type="x" tp:type="Time_In_Us">
        <tp:docstring>
          <p>The new position, in microseconds.</p>
        </tp:docstring>
      </arg>
      <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
        <p>
          Indicates that the track position has changed in a way that is
          inconsistant with the current playing state.
        </p>
        <p>When this signal is not received, clients should assume that:</p>
        <ul>
          <li>
            When playing, the position progresses according to the rate property.
          </li>
          <li>When paused, it remains constant.</li>
        </ul>
        <p>
          This signal does not need to be emitted when playback starts
          or when the track changes, unless the track is starting at an
          unexpected position. An expected position would be the last
          known one when going from Paused to Playing, and 0 when going from
          Stopped to Playing.
        </p>
      </tp:docstring>
    </signal>

  </interface>
</node>
<!-- vim:set sw=2 sts=2 et ft=xml: -->\
"""
    )[0]
    MEDIA_PLAYER_PLAYLISTS_INTERFACE_INTROSPECTION_XML = ElementTree.fromstring(
        """\
<?xml version="1.0" ?>
<node name="/Playlists_Interface" xmlns:tp="http://telepathy.freedesktop.org/wiki/DbusSpec#extensions-v0">
  <interface name="org.mpris.MediaPlayer2.Playlists">
    <tp:added version="2.1" />
    <tp:docstring>
      <p>Provides access to the media player's playlists.</p>
      <p>
        Since D-Bus does not provide an easy way to check for what interfaces
        are exported on an object, clients should attempt to get one of the
        properties on this interface to see if it is implemented.
      </p>
    </tp:docstring>

    <tp:simple-type name="Playlist_Id" type="o" array-name="Playlist_Id_List">
      <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
        <p>Unique playlist identifier.</p>
        <tp:rationale>
          <p>
            Multiple playlists may have the same name.
          </p>
          <p>
            This is a D-Bus object id as that is the definitive way to have
            unique identifiers on D-Bus.  It also allows for future optional
            expansions to the specification where tracks are exported to D-Bus
            with an interface similar to org.gnome.UPnP.MediaItem2.
          </p>
        </tp:rationale>
      </tp:docstring>
    </tp:simple-type>

    <tp:simple-type name="Uri" type="s" array-name="Uri_List">
      <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
        <p>A URI.</p>
      </tp:docstring>
    </tp:simple-type>

    <tp:struct name="Playlist" array-name="Playlist_List">
      <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
        <p>A data structure describing a playlist.</p>
      </tp:docstring>
      <tp:member type="o" tp:type="Playlist_Id" name="Id">
        <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
          <p>A unique identifier for the playlist.</p>
          <p>This should remain the same if the playlist is renamed.</p>
        </tp:docstring>
      </tp:member>
      <tp:member type="s" name="Name">
        <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
          <p>The name of the playlist, typically given by the user.</p>
        </tp:docstring>
      </tp:member>
      <tp:member type="s" tp:type="Uri" name="Icon">
        <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
          <p>The URI of an (optional) icon.</p>
        </tp:docstring>
      </tp:member>
    </tp:struct>

    <tp:struct name="Maybe_Playlist">
      <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
        <p>A data structure describing a playlist, or nothing.</p>
        <tp:rationale>
          <p>
            D-Bus does not (at the time of writing) support a MAYBE type,
            so we are forced to invent our own.
          </p>
        </tp:rationale>
      </tp:docstring>
      <tp:member type="b" name="Valid">
        <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
          <p>Whether this structure refers to a valid playlist.</p>
        </tp:docstring>
      </tp:member>
      <tp:member type="(oss)" tp:type="Playlist" name="Playlist">
        <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
          <p>The playlist, providing Valid is true, otherwise undefined.</p>
          <p>
            When constructing this type, it should be noted that the playlist
            ID must be a valid object path, or D-Bus implementations may reject
            it.  This is true even when Valid is false.  It is suggested that
            "/" is used as the playlist ID in this case.
          </p>
        </tp:docstring>
      </tp:member>
    </tp:struct>

    <tp:enum name="Playlist_Ordering" array-name="Playlist_Ordering_List" type="s">
      <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
        <p>Specifies the ordering of returned playlists.</p>
      </tp:docstring>
      <tp:enumvalue suffix="Alphabetical" value="Alphabetical">
        <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
          <p>Alphabetical ordering by name, ascending.</p>
        </tp:docstring>
      </tp:enumvalue>
      <tp:enumvalue suffix="CreationDate" value="Created">
        <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
          <p>Ordering by creation date, oldest first.</p>
        </tp:docstring>
      </tp:enumvalue>
      <tp:enumvalue suffix="ModifiedDate" value="Modified">
        <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
          <p>Ordering by last modified date, oldest first.</p>
        </tp:docstring>
      </tp:enumvalue>
      <tp:enumvalue suffix="LastPlayDate" value="Played">
        <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
          <p>Ordering by date of last playback, oldest first.</p>
        </tp:docstring>
      </tp:enumvalue>
      <tp:enumvalue suffix="UserDefined" value="User">
        <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
          <p>A user-defined ordering.</p>
          <tp:rationale>
            <p>
              Some media players may allow users to order playlists as they
              wish.  This ordering allows playlists to be retreived in that
              order.
            </p>
          </tp:rationale>
        </tp:docstring>
      </tp:enumvalue>
    </tp:enum>

    <method name="ActivatePlaylist" tp:name-for-bindings="Activate_Playlist">
      <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
        <p>
          Starts playing the given playlist.
        </p>
        <p>
          Note that this must be implemented.  If the media player does not
          allow clients to change the playlist, it should not implement this
          interface at all.
        </p>
        <p>
          It is up to the media player whether this completely replaces the
          current tracklist, or whether it is merely inserted into the
          tracklist and the first track starts.  For example, if the media
          player is operating in a "jukebox" mode, it may just append the
          playlist to the list of upcoming tracks, and skip to the first
          track in the playlist.
        </p>
      </tp:docstring>
      <arg direction="in" name="PlaylistId" type="o">
        <tp:docstring>
          <p>The id of the playlist to activate.</p>
        </tp:docstring>
      </arg>
    </method>

    <method name="GetPlaylists" tp:name-for-bindings="Get_Playlists">
      <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
        <p>Gets a set of playlists.</p>
      </tp:docstring>
      <arg direction="in" name="Index" type="u">
        <tp:docstring>
          <p>The index of the first playlist to be fetched (according to the ordering).</p>
        </tp:docstring>
      </arg>
      <arg direction="in" name="MaxCount" type="u">
        <tp:docstring>
          <p>The maximum number of playlists to fetch.</p>
        </tp:docstring>
      </arg>
      <arg direction="in" name="Order" type="s" tp:type="Playlist_Ordering">
        <tp:docstring>
          <p>The ordering that should be used.</p>
        </tp:docstring>
      </arg>
      <arg direction="in" name="ReverseOrder" type="b">
        <tp:docstring>
          <p>Whether the order should be reversed.</p>
        </tp:docstring>
      </arg>
      <arg direction="out" name="Playlists" type="a(oss)" tp:type="Playlist[]">
        <tp:docstring>
          <p>A list of (at most MaxCount) playlists.</p>
        </tp:docstring>
      </arg>
    </method>

    <property name="PlaylistCount" type="u" tp:name-for-bindings="Playlist_Count" access="read">
      <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="true"/>
      <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
        <p>
          The number of playlists available.
        </p>
      </tp:docstring>
    </property>

    <property name="Orderings" tp:name-for-bindings="Orderings" type="as" tp:type="Playlist_Ordering[]" access="read">
      <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="true"/>
      <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
        <p>
          The available orderings.  At least one must be offered.
        </p>
        <tp:rationale>
          <p>
            Media players may not have access to all the data required for some
            orderings.  For example, creation times are not available on UNIX
            filesystems (don't let the ctime fool you!).  On the other hand,
            clients should have some way to get the "most recent" playlists.
          </p>
        </tp:rationale>
      </tp:docstring>
    </property>

    <property name="ActivePlaylist" type="(b(oss))" tp:name-for-bindings="Active_Playlist" tp:type="Maybe_Playlist" access="read">
      <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="true"/>
      <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
        <p>
          The currently-active playlist.
        </p>
        <p>
          If there is no currently-active playlist, the structure's Valid field
          will be false, and the Playlist details are undefined.
        </p>
        <p>
          Note that this may not have a value even after ActivatePlaylist is
          called with a valid playlist id as ActivatePlaylist implementations
          have the option of simply inserting the contents of the playlist into
          the current tracklist.
        </p>
      </tp:docstring>
    </property>

    <signal name="PlaylistChanged" tp:name-for-bindings="Playlist_Changed">
      <arg name="Playlist" type="(oss)" tp:type="Playlist">
        <tp:docstring>
          The playlist which details have changed.
        </tp:docstring>
      </arg>
      <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
        <p>Indicates that either the Name or Icon attribute of a
           playlist has changed.
        </p>
        <p>Client implementations should be aware that this signal
           may not be implemented.
        </p>
        <tp:rationale>
           Without this signal, media players have no way to notify clients
           of a change in the attributes of a playlist other than the active one
        </tp:rationale>
      </tp:docstring>
    </signal>

  </interface>
</node>
<!-- vim:set sw=2 sts=2 et ft=xml: -->\
"""
    )[0]
    MEDIA_PLAYER_TRACK_LIST_INTERFACE_INTROSPECTION_XML = ElementTree.fromstring(
        """\
<?xml version="1.0" ?>
<node name="/Track_List_Interface" xmlns:tp="http://telepathy.freedesktop.org/wiki/DbusSpec#extensions-v0">
  <interface name="org.mpris.MediaPlayer2.TrackList">

    <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
      <p>
        Provides access to a short list of tracks which were recently played or
        will be played shortly.  This is intended to provide context to the
        currently-playing track, rather than giving complete access to the
        media player's playlist.
      </p>
      <p>
        Example use cases are the list of tracks from the same album as the
        currently playing song or the
        <a href="http://projects.gnome.org/rhythmbox/">Rhythmbox</a> play queue.
      </p>
      <p>
        Each track in the tracklist has a unique identifier.
        The intention is that this uniquely identifies the track within
        the scope of the tracklist. In particular, if a media item
        (a particular music file, say) occurs twice in the track list, each
        occurrence should have a different identifier. If a track is removed
        from the middle of the playlist, it should not affect the track ids
        of any other tracks in the tracklist.
      </p>
      <p>
        As a result, the traditional track identifiers of URLs and position
        in the playlist cannot be used. Any scheme which satisfies the
        uniqueness requirements is valid, as clients should not make any
        assumptions about the value of the track id beyond the fact
        that it is a unique identifier.
      </p>
      <p>
        Note that the (memory and processing) burden of implementing the
        TrackList interface and maintaining unique track ids for the
        playlist can be mitigated by only exposing a subset of the playlist when
        it is very long (the 20 or so tracks around the currently playing
        track, for example). This is a recommended practice as the tracklist
        interface is not designed to enable browsing through a large list of tracks,
        but rather to provide clients with context about the currently playing track.
      </p>
    </tp:docstring>

    <tp:mapping name="Metadata_Map" array-name="Metadata_Map_List">
      <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
        <p>A mapping from metadata attribute names to values.</p>
        <p>
          The <b>mpris:trackid</b> attribute must always be present, and must be
          of D-Bus type "o".  This contains a D-Bus path that uniquely identifies
          the track within the scope of the playlist.  There may or may not be
          an actual D-Bus object at that path; this specification says nothing
          about what interfaces such an object may implement.
        </p>
        <p>
          If the length of the track is known, it should be provided in the
          metadata property with the "mpris:length" key.  The length must be
          given in microseconds, and be represented as a signed 64-bit integer.
        </p>
        <p>
          If there is an image associated with the track, a URL for it may be
          provided using the "mpris:artUrl" key.  For other metadata, fields
          defined by the
          Xesam ontology
          should be used, prefixed by "xesam:".  See the
          <a href="http://www.freedesktop.org/wiki/Specifications/mpris-spec/metadata">metadata page on the freedesktop.org wiki</a>
          for a list of common fields.
        </p>
        <p>
          Lists of strings should be passed using the array-of-string ("as")
          D-Bus type.  Dates should be passed as strings using the ISO 8601
          extended format (eg: 2007-04-29T14:35:51).  If the timezone is
          known, RFC 3339's internet profile should be used (eg:
          2007-04-29T14:35:51+02:00).
        </p>
      </tp:docstring>
      <tp:member type="s" name="Attribute">
        <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
          <p>
            The name of the attribute; see the
            <a href="http://www.freedesktop.org/wiki/Specifications/mpris-spec/metadata">metadata page</a>
            for guidelines on names to use.
          </p>
        </tp:docstring>
      </tp:member>
      <tp:member type="v" name="Value">
        <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
          <p>The value of the attribute, in the most appropriate format.</p>
        </tp:docstring>
      </tp:member>
    </tp:mapping>

    <tp:simple-type name="Uri" type="s">
      <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
        <p>A unique resource identifier.</p>
      </tp:docstring>
    </tp:simple-type>

    <method name="GetTracksMetadata" tp:name-for-bindings="Get_Tracks_Metadata">
      <arg direction="in" name="TrackIds" type="ao" tp:type="Track_Id[]">
        <tp:docstring>
          <p>The list of track ids for which metadata is requested.</p>
        </tp:docstring>
      </arg>
      <arg direction="out" type="aa{sv}" tp:type="Metadata_Map[]" name="Metadata">
        <tp:docstring>
          <p>Metadata of the set of tracks given as input.</p>
          <p>See the type documentation for more details.</p>
        </tp:docstring>
      </arg>
      <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
        <p>Gets all the metadata available for a set of tracks.</p>
        <p>
          Each set of metadata must have a "mpris:trackid" entry at the very least,
          which contains a string that uniquely identifies this track within
          the scope of the tracklist.
        </p>
      </tp:docstring>
    </method>

    <method name="AddTrack" tp:name-for-bindings="Add_Track">
      <arg direction="in" type="s" tp:type="Uri" name="Uri">
        <tp:docstring>
          <p>
            The uri of the item to add. Its uri scheme should be an element of the
            <strong>org.mpris.MediaPlayer2.SupportedUriSchemes</strong>
            property and the mime-type should match one of the elements of the
            <strong>org.mpris.MediaPlayer2.SupportedMimeTypes</strong>
          </p>
        </tp:docstring>
      </arg>
      <arg direction="in" type="o" tp:type="Track_Id" name="AfterTrack">
        <tp:docstring>
          <p>
            The identifier of the track after which
            the new item should be inserted. The path
            <literal>/org/mpris/MediaPlayer2/TrackList/NoTrack</literal>
            indicates that the track should be inserted at the
            start of the track list.
          </p>
        </tp:docstring>
      </arg>
      <arg direction="in" type="b" name="SetAsCurrent">
        <tp:docstring>
          <p>
            Whether the newly inserted track should be considered as
            the current track. Setting this to true has the same effect as
            calling GoTo afterwards.
          </p>
        </tp:docstring>
      </arg>
      <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
        <p>Adds a URI in the TrackList.</p>
        <p>
          If the <tp:member-ref>CanEditTracks</tp:member-ref> property is false,
          this has no effect.
        </p>
        <p>
          Note: Clients should not assume that the track has been added at the
          time when this method returns. They should wait for a TrackAdded (or
          TrackListReplaced) signal.
        </p>
      </tp:docstring>
    </method>

    <method name="RemoveTrack" tp:name-for-bindings="Remove__Track">
      <arg direction="in" type="o" tp:type="Track_Id" name="TrackId">
        <tp:docstring>
          <p>Identifier of the track to be removed.</p>
          <p>
            <literal>/org/mpris/MediaPlayer2/TrackList/NoTrack</literal>
            is <em>not</em> a valid value for this argument.
          </p>
        </tp:docstring>
      </arg>
      <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
        <p>Removes an item from the TrackList.</p>
        <p>If the track is not part of this tracklist, this has no effect.</p>
        <p>
          If the <tp:member-ref>CanEditTracks</tp:member-ref> property is false,
          this has no effect.
        </p>
        <p>
          Note: Clients should not assume that the track has been removed at the
          time when this method returns. They should wait for a TrackRemoved (or
          TrackListReplaced) signal.
        </p>
      </tp:docstring>
    </method>

    <method name="GoTo" tp:name-for-bindings="Go_To">
      <arg direction="in" type="o" tp:type="Track_Id" name="TrackId">
        <tp:docstring>
          <p>Identifier of the track to skip to.</p>
          <p>
            <literal>/org/mpris/MediaPlayer2/TrackList/NoTrack</literal>
            is <em>not</em> a valid value for this argument.
          </p>
        </tp:docstring>
      </arg>
      <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
        <p>Skip to the specified TrackId.</p>
        <p>If the track is not part of this tracklist, this has no effect.</p>
        <p>
          If this object is not <strong>/org/mpris/MediaPlayer2</strong>,
          the current TrackList's tracks should be replaced with the contents of
          this TrackList, and the TrackListReplaced signal should be fired from
          <strong>/org/mpris/MediaPlayer2</strong>.
        </p>
      </tp:docstring>
    </method>

    <property name="Tracks" type="ao" tp:type="Track_Id[]" tp:name-for-bindings="Tracks" access="read">
      <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="invalidates"/>
      <tp:docstring>
        <p>
          An array which contains the identifier of each track
          in the tracklist, in order.
        </p>
        <p>
          The <literal>org.freedesktop.DBus.Properties.PropertiesChanged</literal>
          signal is emited every time this property changes, but the signal
          message does not contain the new value.

          Client implementations should rather rely on the
          <tp:member-ref>TrackAdded</tp:member-ref>,
          <tp:member-ref>TrackRemoved</tp:member-ref> and
          <tp:member-ref>TrackListReplaced</tp:member-ref> signals to keep their
          representation of the tracklist up to date.
        </p>
      </tp:docstring>
    </property>

    <property name="CanEditTracks" type="b" tp:name-for-bindings="Can_Edit_Tracks" access="read">
      <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="true"/>
      <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
        <p>
          If <strong>false</strong>, calling
          <tp:member-ref>AddTrack</tp:member-ref> or
          <tp:member-ref>RemoveTrack</tp:member-ref> will have no effect,
          and may raise a NotSupported error.
        </p>
      </tp:docstring>
    </property>

    <signal name="TrackListReplaced" tp:name-for-bindings="Track_List_Replaced">
      <arg name="Tracks" type="ao" tp:type="Track_Id[]">
        <tp:docstring>
          <p>The new content of the tracklist.</p>
        </tp:docstring>
      </arg>
      <arg name="CurrentTrack" type="o" tp:type="Track_Id">
        <tp:docstring>
          <p>The identifier of the track to be considered as current.</p>
          <p>
            <literal>/org/mpris/MediaPlayer2/TrackList/NoTrack</literal>
            indicates that there is no current track.
          </p>
          <p>
            This should correspond to the <literal>mpris:trackid</literal> field of the
            Metadata property of the <literal>org.mpris.MediaPlayer2.Player</literal>
            interface.
          </p>
        </tp:docstring>
      </arg>
      <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
        <p>Indicates that the entire tracklist has been replaced.</p>
        <p>
          It is left up to the implementation to decide when
          a change to the track list is invasive enough that
          this signal should be emitted instead of a series of
          TrackAdded and TrackRemoved signals.
        </p>
      </tp:docstring>
    </signal>

    <signal name="TrackAdded" tp:name-for-bindings="Track_Added">
      <arg type="a{sv}" tp:type="Metadata_Map" name="Metadata">
        <tp:docstring>
          <p>The metadata of the newly added item.</p>
          <p>This must include a mpris:trackid entry.</p>
          <p>See the type documentation for more details.</p>
        </tp:docstring>
      </arg>
      <arg type="o" tp:type="Track_Id" name="AfterTrack">
        <tp:docstring>
          <p>
            The identifier of the track after which the new track
            was inserted. The path
            <literal>/org/mpris/MediaPlayer2/TrackList/NoTrack</literal>
            indicates that the track was inserted at the
            start of the track list.
          </p>
        </tp:docstring>
      </arg>
      <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
        <p>Indicates that a track has been added to the track list.</p>
      </tp:docstring>
    </signal>

    <signal name="TrackRemoved" tp:name-for-bindings="Track_Removed">
      <arg type="o" tp:type="Track_Id" name="TrackId">
        <tp:docstring>
          <p>The identifier of the track being removed.</p>
          <p>
            <literal>/org/mpris/MediaPlayer2/TrackList/NoTrack</literal>
            is <em>not</em> a valid value for this argument.
          </p>
        </tp:docstring>
      </arg>
      <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
        <p>Indicates that a track has been removed from the track list.</p>
      </tp:docstring>
    </signal>

    <signal name="TrackMetadataChanged" tp:name-for-bindings="Track_Metadata_Changed">
      <arg type="o" tp:type="Track_Id" name="TrackId">
        <tp:docstring>
          <p>The id of the track which metadata has changed.</p>
          <p>If the track id has changed, this will be the old value.</p>
          <p>
            <literal>/org/mpris/MediaPlayer2/TrackList/NoTrack</literal>
            is <em>not</em> a valid value for this argument.
          </p>
        </tp:docstring>
      </arg>
      <arg type="a{sv}" tp:type="Metadata_Map" name="Metadata">
        <tp:docstring>
          <p>The new track metadata.</p>
          <p>
            This must include a mpris:trackid entry.  If the track id has
            changed, this will be the new value.
          </p>
          <p>See the type documentation for more details.</p>
        </tp:docstring>
      </arg>
      <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
        <p>
          Indicates that the metadata of a track in the tracklist has changed.
        </p>
        <p>
          This may indicate that a track has been replaced, in which case the
          mpris:trackid metadata entry is different from the TrackId argument.
        </p>
      </tp:docstring>
    </signal>

  </interface>
</node>
<!-- vim:set sw=2 sts=2 et ft=xml: -->\
"""
    )[0]
    MEDIA_PLAYER_MEDIA_PLAYER_INTERFACE_INTROSPECTION_XML = ElementTree.fromstring(
        """\
<?xml version="1.0" ?>
<node name="/Media_Player" xmlns:tp="http://telepathy.freedesktop.org/wiki/DbusSpec#extensions-v0">
  <interface name="org.mpris.MediaPlayer2">
    <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="true"/>

    <method name="Raise" tp:name-for-bindings="Raise">
      <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
        <p>
          Brings the media player's user interface to the front using any
          appropriate mechanism available.
        </p>
        <p>
          The media player may be unable to control how its user interface
          is displayed, or it may not have a graphical user interface at all.
          In this case, the <tp:member-ref>CanRaise</tp:member-ref> property is
          <strong>false</strong> and this method does nothing.
        </p>
      </tp:docstring>
    </method>

    <method name="Quit" tp:name-for-bindings="Quit">
      <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
        <p>Causes the media player to stop running.</p>
        <p>
          The media player may refuse to allow clients to shut it down.
          In this case, the <tp:member-ref>CanQuit</tp:member-ref> property is
          <strong>false</strong> and this method does nothing.
        </p>
        <p>
          Note: Media players which can be D-Bus activated, or for which there is
          no sensibly easy way to terminate a running instance (via the main
          interface or a notification area icon for example) should allow clients
          to use this method. Otherwise, it should not be needed.
        </p>
        <p>If the media player does not have a UI, this should be implemented.</p>
      </tp:docstring>
    </method>

    <property name="CanQuit" type="b" tp:name-for-bindings="Can_Quit" access="read">
      <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
        <p>
          If <strong>false</strong>, calling
          <tp:member-ref>Quit</tp:member-ref> will have no effect, and may
          raise a NotSupported error.  If <strong>true</strong>, calling
          <tp:member-ref>Quit</tp:member-ref> will cause the media application
          to attempt to quit (although it may still be prevented from quitting
          by the user, for example).
        </p>
      </tp:docstring>
    </property>

    <property name="Fullscreen" type="b" tp:name-for-bindings="Fullscreen" access="readwrite">
      <tp:added version="2.2" />
      <annotation name="org.mpris.MediaPlayer2.property.optional" value="true"/>
      <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
        <p>Whether the media player is occupying the fullscreen.</p>
        <p>
          This is typically used for videos.  A value of <strong>true</strong>
          indicates that the media player is taking up the full screen.
        </p>
        <p>
          Media centre software may well have this value fixed to <strong>true</strong>
        </p>
        <p>
          If <tp:member-ref>CanSetFullscreen</tp:member-ref> is <strong>true</strong>,
          clients may set this property to <strong>true</strong> to tell the media player
          to enter fullscreen mode, or to <strong>false</strong> to return to windowed
          mode.
        </p>
        <p>
          If <tp:member-ref>CanSetFullscreen</tp:member-ref> is <strong>false</strong>,
          then attempting to set this property should have no effect, and may raise
          an error.  However, even if it is <strong>true</strong>, the media player
          may still be unable to fulfil the request, in which case attempting to set
          this property will have no effect (but should not raise an error).
        </p>
        <tp:rationale>
          <p>
            This allows remote control interfaces, such as LIRC or mobile devices like
            phones, to control whether a video is shown in fullscreen.
          </p>
        </tp:rationale>
      </tp:docstring>
    </property>

    <property name="CanSetFullscreen" type="b" tp:name-for-bindings="Can_Set_Fullscreen" access="read">
      <tp:added version="2.2" />
      <annotation name="org.mpris.MediaPlayer2.property.optional" value="true"/>
      <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
        <p>
          If <strong>false</strong>, attempting to set
          <tp:member-ref>Fullscreen</tp:member-ref> will have no effect, and may
          raise an error.  If <strong>true</strong>, attempting to set
          <tp:member-ref>Fullscreen</tp:member-ref> will not raise an error, and (if it
          is different from the current value) will cause the media player to attempt to
          enter or exit fullscreen mode.
        </p>
        <p>
          Note that the media player may be unable to fulfil the request.
          In this case, the value will not change.  If the media player knows in
          advance that it will not be able to fulfil the request, however, this
          property should be <strong>false</strong>.
        </p>
        <tp:rationale>
          <p>
            This allows clients to choose whether to display controls for entering
            or exiting fullscreen mode.
          </p>
        </tp:rationale>
      </tp:docstring>
    </property>

    <property name="CanRaise" type="b" tp:name-for-bindings="Can_Raise" access="read">
      <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
        <p>
          If <strong>false</strong>, calling
          <tp:member-ref>Raise</tp:member-ref> will have no effect, and may
          raise a NotSupported error.  If <strong>true</strong>, calling
          <tp:member-ref>Raise</tp:member-ref> will cause the media application
          to attempt to bring its user interface to the front, although it may
          be prevented from doing so (by the window manager, for example).
        </p>
      </tp:docstring>
    </property>

    <property name="HasTrackList" type="b" tp:name-for-bindings="Has_TrackList" access="read">
      <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
        <p>
          Indicates whether the <strong>/org/mpris/MediaPlayer2</strong>
          object implements the <strong>org.mpris.MediaPlayer2.TrackList</strong>
          interface.
        </p>
      </tp:docstring>
    </property>

    <property name="Identity" type="s" tp:name-for-bindings="Identity" access="read">
      <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
        <p>A friendly name to identify the media player to users.</p>
        <p>This should usually match the name found in .desktop files</p>
        <p>(eg: "VLC media player").</p>
      </tp:docstring>
    </property>

    <property name="DesktopEntry" type="s" tp:name-for-bindings="Desktop_Entry" access="read">
      <annotation name="org.mpris.MediaPlayer2.property.optional" value="true"/>
      <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
        <p>The basename of an installed .desktop file which complies with the <a href="http://standards.freedesktop.org/desktop-entry-spec/latest/">Desktop entry specification</a>,
        with the ".desktop" extension stripped.</p>
        <p>
          Example: The desktop entry file is "/usr/share/applications/vlc.desktop",
          and this property contains "vlc"
        </p>
      </tp:docstring>
    </property>

    <property name="SupportedUriSchemes" type="as" tp:name-for-bindings="Supported_Uri_Schemes" access="read">
      <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
        <p>
          The URI schemes supported by the media player.
        </p>
        <p>
          This can be viewed as protocols supported by the player in almost
          all cases.  Almost every media player will include support for the
          "file" scheme.  Other common schemes are "http" and "rtsp".
        </p>
        <p>
          Note that URI schemes should be lower-case.
        </p>
        <tp:rationale>
          <p>
            This is important for clients to know when using the editing
            capabilities of the Playlist interface, for example.
          </p>
        </tp:rationale>
      </tp:docstring>
    </property>

    <property name="SupportedMimeTypes" type="as" tp:name-for-bindings="Supported_Mime_Types" access="read">
      <tp:docstring xmlns="http://www.w3.org/1999/xhtml">
        <p>
          The mime-types supported by the media player.
        </p>
        <p>
          Mime-types should be in the standard format (eg: audio/mpeg or
          application/ogg).
        </p>
        <tp:rationale>
          <p>
            This is important for clients to know when using the editing
            capabilities of the Playlist interface, for example.
          </p>
        </tp:rationale>
      </tp:docstring>
    </property>

  </interface>
</node>
<!-- vim:set sw=2 sts=2 et ft=xml: -->\
"""
    )[0]

    def on_new_bus(name):
        name_match = MEDIA_PLAYER_BUS_NAME_REGEX.fullmatch(name)
        if not name_match:
            return
        bus_name = name_match.group(1)
        media_player_busses.add(bus_name)
        if bus_name in watch_media_player_task_closers:
            # This means the previous 'watch_media_player_task' on the same
            # 'bus_name' is still running. When it finishes it will restart
            # itself in 'on_complete' if 'bus_name' is still owned.
            return

        def create_task():
            shutdown_signal = asyncio.Event()
            watch_media_player_task_closers[bus_name] = shutdown_signal
            watch_media_player_task = task_group.create_task(
                watch_media_player_forever(
                    message_bus,
                    media_player_object_introspection,
                    bus_name,
                    task_group,
                    bar_event_queue,
                    shutdown_signal,
                )
            )
            watch_media_player_task.add_done_callback(on_complete)

        def on_complete(task):
            del watch_media_player_task_closers[bus_name]
            if task.cancelled:
                return
            if bus_name in media_player_busses:
                create_task()

        create_task()

    def on_remove_bus(name):
        name_match = MEDIA_PLAYER_BUS_NAME_REGEX.fullmatch(name)
        if not name_match:
            return
        bus_name = name_match.group(1)
        media_player_busses.remove(bus_name)
        if bus_name not in watch_media_player_task_closers:
            return
        shutdown_signal = watch_media_player_task_closers[bus_name]
        if not shutdown_signal.is_set():
            shutdown_signal.set()

    def on_name_owner_changed(bus_name, old_owner, new_owner):
        if not initialized:
            return
        handler = on_new_bus if new_owner else on_remove_bus
        handler(bus_name)

    def list_names_callback(error, bus_names):
        if error:
            raise error
        nonlocal initialized
        initialized = True
        for bus_name in bus_names:
            on_new_bus(bus_name)

    interfaces = [
        MEDIA_PLAYER_PLAYER_INTERFACE_INTROSPECTION_XML,
        MEDIA_PLAYER_PLAYLISTS_INTERFACE_INTROSPECTION_XML,
        MEDIA_PLAYER_TRACK_LIST_INTERFACE_INTROSPECTION_XML,
        MEDIA_PLAYER_MEDIA_PLAYER_INTERFACE_INTROSPECTION_XML,
    ]
    media_player_object_introspection = Node.default()
    media_player_object_introspection.interfaces.extend(
        Interface.from_xml(interface) for interface in interfaces
    )
    message_bus = await MessageBus().connect()
    dbus_object_introspection = await message_bus.introspect(
        DBUS_BUS_NAME, DBUS_OBJECT_PATH
    )
    dbus_object = message_bus.get_proxy_object(
        DBUS_BUS_NAME, DBUS_OBJECT_PATH, dbus_object_introspection
    )
    dbus_interface = dbus_object.get_interface(DBUS_INTERFACE)
    media_player_busses = set()
    watch_media_player_task_closers = {}
    initialized = False
    dbus_interface.on_name_owner_changed(on_name_owner_changed)
    dbus_call_method_with_response_callback(
        dbus_interface, "ListNames", list_names_callback
    )


async def watch_media_player_forever(
    message_bus,
    media_player_object_introspection,
    media_player_dbus_name,
    task_group,
    bar_event_queue,
    shutdown_signal,
):
    # documentation for MPRIS Player interface:
    # https://specifications.freedesktop.org/mpris-spec/latest/Player_Interface.html

    MEDIA_PLAYER_BUS_NAME = f"org.mpris.MediaPlayer2.{media_player_dbus_name}"
    MEDIA_PLAYER_OBJECT_PATH = "/org/mpris/MediaPlayer2"
    PROPERTIES_INTERFACE = "org.freedesktop.DBus.Properties"
    MEDIA_PLAYER_PLAYER_INTERFACE = "org.mpris.MediaPlayer2.Player"

    def on_seeked(new_position):
        if media_player_state is None:
            # we must wait for the 'GetAll' method response
            return
        old_track_current_second = media_player_state.track_current_second
        media_player_state.seek(new_position)
        if media_player_state.is_playing():
            media_player_state.restart_clock()
        if old_track_current_second != media_player_state.track_current_second:
            media_player_state.send_update()

    def on_properties_changed(
        interface_name, changed_properties, invalidated_properties
    ):
        if media_player_state is None:
            # we must wait for the 'GetAll' method response
            return
        if interface_name != MEDIA_PLAYER_PLAYER_INTERFACE:
            return
        should_update = False
        for changed_property, value_variant in changed_properties.items():
            value = value_variant.value
            match changed_property:
                case "PlaybackStatus":
                    was_playing = media_player_state.is_playing()
                    was_paused = media_player_state.is_paused()
                    was_stopped = media_player_state.is_stopped()
                    is_playing = value == "Playing"
                    if was_playing and is_playing:
                        # hack: cmus doesn't send seek signal when triggering
                        # 'player-prev' seeks to the beginning of the track
                        # (happens when the position in track is less than
                        # 'rewind_offset'). However, cmus does for some reason
                        # set 'PlaybackStatus' to 'Playing', so we detect this
                        # here and manually seek.
                        old_track_current_second = (
                            media_player_state.track_current_second
                        )
                        media_player_state.seek(0)
                        media_player_state.restart_clock()
                        if (
                            old_track_current_second
                            != media_player_state.track_current_second
                        ):
                            should_update = True
                        continue
                    match value:
                        case "Playing":
                            media_player_state.restart_clock()
                            should_update = True
                        case "Paused":
                            if was_playing:
                                media_player_state.cancel_clock()
                                media_player_state.update_last_known_position_to_estimated_track_current_position()
                            if not was_paused:
                                should_update = True
                        case "Stopped":
                            if was_playing:
                                media_player_state.cancel_clock()
                            if not was_stopped:
                                media_player_state.seek(0)
                                should_update = True
                    media_player_state.playback_status = value
                case "Metadata":
                    old_track_id = media_player_state.track_id
                    old_track_length = media_player_state.track_length
                    old_track_title = media_player_state.track_title
                    old_visible_metadata = media_player_state.get_visible_metadata()
                    media_player_state.set_metadata(value)
                    # hack: Firefox doesn't change 'track_id' when switching
                    # tracks so we also consider a title change a track switch
                    switched_track = (
                        old_track_id != media_player_state.track_id
                        or old_track_title != media_player_state.track_title
                    )
                    changed_track_length = (
                        old_track_length != media_player_state.track_length
                    )
                    visible_metadata_changed = (
                        old_visible_metadata
                        != media_player_state.get_visible_metadata()
                    )
                    old_track_current_second = media_player_state.track_current_second
                    if switched_track:
                        media_player_state.seek(0)
                        if media_player_state.is_playing():
                            media_player_state.restart_clock()
                    elif changed_track_length:
                        # 'update_last_known_position_to_estimated_track_current_position'
                        # handles 'track_length' becoming shorter than the
                        # current position or 'track_length' becoming larger
                        # when 'track_hit_end' is true. It clamps the position
                        # and updates 'track_hit_end' according to the new
                        # 'track_length'.
                        media_player_state.update_last_known_position_to_estimated_track_current_position()
                        if media_player_state.is_playing():
                            media_player_state.restart_clock()
                    track_current_second_changed = (
                        old_track_current_second
                        != media_player_state.track_current_second
                    )
                    if track_current_second_changed or visible_metadata_changed:
                        should_update = True
                case "LoopStatus":
                    if media_player_state.loop_status != value:
                        media_player_state.loop_status = value
                        should_update = True
                case "Rate":
                    if value == 0 or media_player_state.rate == value:
                        continue
                    if media_player_state.is_playing():
                        media_player_state.update_last_known_position_to_estimated_track_current_position()
                    media_player_state.rate = value
                    if media_player_state.is_playing():
                        media_player_state.restart_clock()
        if should_update:
            media_player_state.send_update()

    def disable_signals():
        player_interface.off_seeked(on_seeked)
        properties_interface.off_properties_changed(on_properties_changed)

    def get_all_callback(error, properties):
        initialized_future.set_result(error)
        if error:
            return
        nonlocal media_player_state
        media_player_state = MediaPlayerState(
            media_player_dbus_name, properties, task_group, bar_event_queue
        )

    media_player_state = None
    media_player_object = message_bus.get_proxy_object(
        MEDIA_PLAYER_BUS_NAME,
        MEDIA_PLAYER_OBJECT_PATH,
        media_player_object_introspection,
    )
    player_interface = media_player_object.get_interface(MEDIA_PLAYER_PLAYER_INTERFACE)
    properties_interface = media_player_object.get_interface(PROPERTIES_INTERFACE)
    player_interface.on_seeked(on_seeked)
    properties_interface.on_properties_changed(on_properties_changed)
    initialized_future = asyncio.get_running_loop().create_future()
    dbus_call_method_with_response_callback(
        properties_interface,
        "GetAll",
        get_all_callback,
        MEDIA_PLAYER_PLAYER_INTERFACE,
    )
    try:
        async with asyncio.timeout(2**4):
            error_initializing = await initialized_future
    except TimeoutError:
        # the music player may have never responded
        disable_signals()
        await shutdown_signal.wait()
        return
    if error_initializing:
        # the 'GetAll' method may have failed or the response may have a
        # different signature
        disable_signals()
    await shutdown_signal.wait()
    if not error_initializing:
        disable_signals()
        media_player_state.shutdown()


def dbus_call_method_with_response_callback(interface, method_name, callback, *args):
    # This method avoids race conditions where a DBUS method is retrieving some
    # state and signals are used to notify clients of modifications to that
    # state. Since the 'get_*' methods are awaiting a 'Future' to be completed
    # by the message handler task, the calling task is not guaranteed to be
    # scheduled after receiving the result of the method before some signal is
    # received that modifies the state. Upon receiving this signal, it is not
    # known whether the signal represents a modification to the state before or
    # after the state snapshot retrieved from the 'get_*' method. Handling the
    # result of the method synchronously in the message handler task (same as
    # the signal handlers) avoids this race condition.

    # 'dbus_call_method_with_response_callback' sadly must use internal
    # 'dbus-next' code so it may break on different 'dbus-next' versions

    def on_response(reply, error):
        if error:
            callback(error, None)
        BaseProxyInterface._check_method_return(
            reply, method_introspection.out_signature
        )
        out_len = len(method_introspection.out_args)
        body = replace_idx_with_fds(reply.signature_tree, reply.body, reply.unix_fds)
        result = None
        if out_len:
            if out_len == 1:
                result = body[0]
            else:
                result = body
        callback(None, result)

    try:
        method_introspection = next(
            method
            for method in interface.introspection.methods
            if method.name == method_name
        )
    except StopIteration:
        callback(
            Exception(
                f"{method_name} method not found on interface {interface.introspection.name}"
            ),
            None,
        )
        return
    input_body, unix_fds = replace_fds_with_idx(
        method_introspection.in_signature, list(args)
    )
    flags = MessageFlag.NONE
    msg = Message(
        destination=interface.bus_name,
        path=interface.path,
        interface=interface.introspection.name,
        member=method_introspection.name,
        signature=method_introspection.in_signature,
        body=input_body,
        flags=flags,
        unix_fds=unix_fds,
    )
    interface.bus._call(msg, on_response)


async def watch_sway_forever(bar_event_queue):
    class MessageType(IntEnum):
        GET_WORKSPACES = 1
        SUBSCRIBE = 2
        WORKSPACE_EVENT = 0x80000000

    """
    1. GET_WORKSPACES
       MESSAGE
       Retrieves the list of workspaces.
       REPLY
       The reply is an array of objects corresponding to each workspace. Each
       object has the following properties:
       ┌──────────┬───────────┬─────────────────────────────────────────┐
       │ PROPERTY │ DATA TYPE │               DESCRIPTION               │
       ├──────────┼───────────┼─────────────────────────────────────────┤
       │   num    │  integer  │ The  workspace  number  or -1 for work- │
       │          │           │ spaces that do not start with a number  │
       ├──────────┼───────────┼─────────────────────────────────────────┤
       │   name   │  string   │ The name of the workspace               │
       ├──────────┼───────────┼─────────────────────────────────────────┤
       │ visible  │  boolean  │ Whether the workspace is currently vis- │
       │          │           │ ible on any output                      │
       ├──────────┼───────────┼─────────────────────────────────────────┤
       │ focused  │  boolean  │ Whether the workspace is currently  fo- │
       │          │           │ cused by the default seat (seat0)       │
       ├──────────┼───────────┼─────────────────────────────────────────┤
       │  urgent  │  boolean  │ Whether a view on the workspace has the │
       │          │           │ urgent flag set                         │
       ├──────────┼───────────┼─────────────────────────────────────────┤
       │   rect   │  object   │ The  bounds  of  the workspace. It con- │
       │          │           │ sists of x, y, width, and height        │
       ├──────────┼───────────┼─────────────────────────────────────────┤
       │  output  │  string   │ The name of the output that  the  work- │
       │          │           │ space is on                             │
       └──────────┴───────────┴─────────────────────────────────────────┘

    2. SUBSCRIBE
       MESSAGE
       Subscribe this IPC connection to the event types specified in the
       message payload. The payload should be a valid JSON array of events. See
       the EVENTS section for the list of supported events.
       REPLY
       A single object that contains the property success, which is a boolean
       value indicating whether the subscription was successful or not.

    0x80000000. WORKSPACE
       Sent whenever a change involving a workspace occurs. The event consists
       of a single object with the following properties:
       ┌──────────┬───────────┬─────────────────────────────────────────┐
       │ PROPERTY │ DATA TYPE │               DESCRIPTION               │
       ├──────────┼───────────┼─────────────────────────────────────────┤
       │  change  │  string   │ The  type  of change that occurred. See │
       │          │           │ below for more information              │
       ├──────────┼───────────┼─────────────────────────────────────────┤
       │ current  │  object   │ An object  representing  the  workspace │
       │          │           │ effected or null for reload changes     │
       ├──────────┼───────────┼─────────────────────────────────────────┤
       │   old    │  object   │ For  a focus change, this is will be an │
       │          │           │ object representing the workspace being │
       │          │           │ switched from. Otherwise, it is null    │
       └──────────┴───────────┴─────────────────────────────────────────┘
       The following change types are currently available:
       ┌────────┬──────────────────────────────────────────────────────┐
       │  TYPE  │                     DESCRIPTION                      │
       ├────────┼──────────────────────────────────────────────────────┤
       │  init  │ The workspace was created                            │
       ├────────┼──────────────────────────────────────────────────────┤
       │ empty  │ The workspace is empty and is being destroyed  since │
       │        │ it is not visible                                    │
       ├────────┼──────────────────────────────────────────────────────┤
       │ focus  │ The  workspace was focused. See the old property for │
       │        │ the previous focus                                   │
       ├────────┼──────────────────────────────────────────────────────┤
       │  move  │ The workspace was moved to a different output        │
       ├────────┼──────────────────────────────────────────────────────┤
       │ rename │ The workspace was renamed                            │
       ├────────┼──────────────────────────────────────────────────────┤
       │ urgent │ A view on the workspace has had their  urgency  hint │
       │        │ set  or all urgency hints for views on the workspace │
       │        │ have been cleared                                    │
       ├────────┼──────────────────────────────────────────────────────┤
       │ reload │ The configuration file has been reloaded             │
       └────────┴──────────────────────────────────────────────────────┘
    """

    MAGIC_BYTES = b"i3-ipc"
    MESSAGE_HEADER_STRUCT = struct.Struct(f"={len(MAGIC_BYTES)}sII")

    async def read_message(reader):
        message_header_bytes = await reader.readexactly(MESSAGE_HEADER_STRUCT.size)
        magic_bytes, payload_length, payload_type = MESSAGE_HEADER_STRUCT.unpack(
            message_header_bytes
        )
        assert magic_bytes == MAGIC_BYTES
        payload_bytes = await reader.readexactly(payload_length)
        return payload_type, json.loads(payload_bytes.decode("utf-8"))

    async def send_message(writer, payload_type, payload):
        writer.write(
            MESSAGE_HEADER_STRUCT.pack(MAGIC_BYTES, len(payload), payload_type)
        )
        writer.write(payload)
        await writer.drain()

    async def subscribe(reader, writer, event_types):
        event_types_json = json.dumps(event_types)
        await send_message(
            writer, MessageType.SUBSCRIBE, event_types_json.encode("utf-8")
        )
        payload_type, response = await read_message(reader)
        assert payload_type == MessageType.SUBSCRIBE
        assert response["success"]

    async def send_get_workspaces_message(writer):
        await send_message(writer, MessageType.GET_WORKSPACES, b"")

    def extract_relevant_workspace_data(workspace):
        return {key: workspace[key] for key in ("id", "name", "num", "focused")}

    def sort_workspaces():
        # Primarily sort based on 'num'. For breaking ties, sort by 'name'. Put
        # all workspaces with a 'num' of -1 at end of list.
        workspaces.sort(
            key=lambda workspace: (
                (workspace["num"] + 1 or math.inf) - 1,
                workspace["name"],
            )
        )

    reader, writer = await asyncio.open_unix_connection(path=os.environ["SWAYSOCK"])
    relevant_events = ["workspace"]
    await subscribe(reader, writer, relevant_events)
    await send_get_workspaces_message(writer)
    workspaces = []
    workspaces_initialized = False
    while True:
        payload_type, response = await read_message(reader)
        should_update = False
        match payload_type:
            case MessageType.GET_WORKSPACES:
                old_workspaces = workspaces
                workspaces = [
                    extract_relevant_workspace_data(workspace) for workspace in response
                ]
                sort_workspaces()
                if old_workspaces != workspaces:
                    should_update = True
                workspaces_initialized = True
            case MessageType.WORKSPACE_EVENT:
                if not workspaces_initialized:
                    continue
                should_update = True
                old_event_workspace = response["old"]
                current_event_workspace = response["current"]
                match response["change"]:
                    case "init":
                        workspaces.append(
                            extract_relevant_workspace_data(current_event_workspace)
                        )
                        sort_workspaces()
                    case "empty":
                        workspaces = [
                            workspace
                            for workspace in workspaces
                            if workspace["id"] != current_event_workspace["id"]
                        ]
                    case "focus":
                        found_old = found_current = False
                        for workspace in workspaces:
                            if (
                                not found_old
                                and workspace["id"] == old_event_workspace["id"]
                            ):
                                workspace["focused"] = False
                                found_old = True
                            elif (
                                not found_current
                                and workspace["id"] == current_event_workspace["id"]
                            ):
                                workspace["focused"] = True
                                found_current = True
                            if found_old and found_current:
                                break
                    case "rename":
                        for workspace in workspaces:
                            if workspace["id"] != current_event_workspace["id"]:
                                continue
                            workspace["name"] = current_event_workspace["name"]
                            sort_workspaces()
                            break
                    case _:
                        should_update = False
        if should_update:
            bar_event_queue.put_nowait(
                BarEvent(BarEventType.WORKSPACES_UPDATE, deepcopy(workspaces))
            )


async def run_clock_forever(bar_event_queue):
    def update_time():
        bar_event_queue.put_nowait(
            BarEvent(BarEventType.CLOCK_UPDATE, displayed_second)
        )

    current_time = time.time_ns()
    displayed_second = current_time // 1_000_000_000
    update_time()
    while True:
        current_time = time.time_ns()
        current_second = current_time // 1_000_000_000
        next_second_to_display = max(
            displayed_second + 1,
            current_second + 1,
        )
        displayed_second_is_more_than_one_second_behind = (
            displayed_second < next_second_to_display - 1
        )
        if displayed_second_is_more_than_one_second_behind:
            # this could theoretically happen if the event loop was blocked for
            # a long time
            displayed_second = next_second_to_display - 1
            update_time()
        next_second_to_display_nanos = next_second_to_display * 1_000_000_000
        time_till_next_second_to_display_seconds = (
            next_second_to_display_nanos - current_time
        ) / 1_000_000_000
        if time_till_next_second_to_display_seconds > 0:
            await asyncio.sleep(time_till_next_second_to_display_seconds)
        displayed_second += 1
        update_time()


async def update_bar_forever(bar_event_queue):
    SECONDS_IN_MINUTE = 60
    SECONDS_IN_HOUR = 60 * 60
    SEPARATOR = "│"
    SEPARATOR_BYTES = SEPARATOR.encode("utf-8")
    VERTICAL_SINGLE_LEFT_BYTES = "┤".encode("utf-8")
    VERTICAL_DOUBLE_LEFT_BYTES = "╡".encode("utf-8")
    VERTICAL_SINGLE_RIGHT_BYTES = "├".encode("utf-8")
    VERTICAL_DOUBLE_RIGHT_BYTES = "╞".encode("utf-8")
    DOUBLE_HORIZONTAL_BYTES = "═".encode("utf-8")
    SINGLE_HORIZONTAL_BYTES = "─".encode("utf-8")
    ESCAPE = b"\x1b"
    CSI_START = ESCAPE + b"["
    CLEAR_LINE = CSI_START + b"2K"
    CURSOR_CHARACTER_ABSOLUTE_TEMPLATE = CSI_START + b"%bG"
    HIDE_CURSOR = CSI_START + b"?25l"
    SYNCHRONIZED_UPDATE_TEMPLATE = CSI_START + b"?2026%b"
    BEGIN_SYNCHRONIZED_UPDATE = SYNCHRONIZED_UPDATE_TEMPLATE % b"h"
    END_SYNCHRONIZED_UPDATE = SYNCHRONIZED_UPDATE_TEMPLATE % b"l"
    CHARACTER_ATTRIBUTES_TEMPLATE = CSI_START + b"%bm"
    DARK_BACKGROUND = CHARACTER_ATTRIBUTES_TEMPLATE % b"48;2;40;40;40"
    GRAY_BACKGROUND = CHARACTER_ATTRIBUTES_TEMPLATE % b"48;2;189;174;147"
    LIGHT_GRAY_BACKGROUND = CHARACTER_ATTRIBUTES_TEMPLATE % b"48;2;213;196;161"
    WHITE_BACKGROUND = CHARACTER_ATTRIBUTES_TEMPLATE % b"48;2;251;241;199"
    BLACK_FOREGROUND = CHARACTER_ATTRIBUTES_TEMPLATE % b"38;2;0;0;0"
    DARK_GRAY_FOREGROUND = CHARACTER_ATTRIBUTES_TEMPLATE % b"38;2;60;56;54"
    GRAY_FOREGROUND = CHARACTER_ATTRIBUTES_TEMPLATE % b"38;2;146;131;116"
    LIGHT_GRAY_FOREGROUND = CHARACTER_ATTRIBUTES_TEMPLATE % b"38;2;235;219;178"
    BOLD = CHARACTER_ATTRIBUTES_TEMPLATE % b"1"
    NOT_BOLD = CHARACTER_ATTRIBUTES_TEMPLATE % b"22"
    PLAYBACK_STATUS_PRIORITY = {"Playing": 0, "Paused": 1, "Stopped": 2}
    PLAYBACK_STATUS_SPECIFIER = {"Playing": "󰐊", "Paused": "󰏤", "Stopped": "󰓛"}

    def jump_to_column(column):
        writer.write(CURSOR_CHARACTER_ABSOLUTE_TEMPLATE % str(column).encode("utf-8"))

    def format_second_duration(seconds):
        assert seconds >= 0
        if seconds == math.inf:
            return "inf"
        hours = seconds // SECONDS_IN_HOUR
        seconds -= hours * SECONDS_IN_HOUR
        minutes = seconds // SECONDS_IN_MINUTE
        seconds -= minutes * SECONDS_IN_MINUTE
        hours_specifier = f"{hours:02}:" if hours else ""
        minutes_specifier = f"{minutes:02}:"
        seconds_specifier = f"{seconds:02}"
        return f"{hours_specifier}{minutes_specifier}{seconds_specifier}"

    def clamp(value, min_value, max_value):
        return max(min_value, min(max_value, value))

    def on_resize(*args):
        nonlocal terminal_width
        old_terminal_width = terminal_width
        terminal_width = shutil.get_terminal_size().columns
        assert terminal_width > 0
        bar_event_queue.put_nowait(BarEvent(BarEventType.RESIZE, None))

    terminal_width = shutil.get_terminal_size().columns
    loop = asyncio.get_running_loop()
    loop.add_signal_handler(signal.SIGWINCH, on_resize)
    write_transport, write_protocol = await loop.connect_write_pipe(
        asyncio.streams.FlowControlMixin, sys.stdout
    )
    writer = asyncio.StreamWriter(write_transport, write_protocol, None, loop)
    media_players = {}
    media_player_to_show = None
    formatted_media_player_bytes = None
    formatted_media_player_width = None
    formatted_workspaces_bytes = None
    formatted_workspaces_width = None
    formatted_datetime_bytes = None
    formatted_datetime_width = None
    writer.write(HIDE_CURSOR)
    await writer.drain()
    while True:
        bar_event = await bar_event_queue.get()
        if bar_event.event_type.is_media_player_event():
            event_media_player = bar_event.payload["dbus_name"]
        match bar_event.event_type:
            case (
                BarEventType.INITIALIZE_MEDIA_PLAYER
                | BarEventType.UPDATE_MEDIA_PLAYER_STATE
            ):
                media_players[event_media_player] = bar_event.payload
            case BarEventType.SHUTDOWN_MEDIA_PLAYER:
                del media_players[event_media_player]
            case BarEventType.WORKSPACES_UPDATE:
                workspaces = bar_event.payload
                formatted_workspaces_width = (
                    sum(wcwidth.wcswidth(workspace["name"]) for workspace in workspaces)
                    + len(workspaces) * 2
                )
                formatted_workspaces_bytes = bytearray()
                for i, workspace in enumerate(workspaces):
                    focused = workspace["focused"]
                    formatted_workspaces_bytes.extend(BOLD)
                    if focused:
                        formatted_workspaces_bytes.extend(LIGHT_GRAY_FOREGROUND)
                        formatted_workspaces_bytes.extend(DARK_BACKGROUND)
                    elif i % 2 == 1:
                        formatted_workspaces_bytes.extend(GRAY_BACKGROUND)
                    else:
                        formatted_workspaces_bytes.extend(DARK_GRAY_FOREGROUND)
                        formatted_workspaces_bytes.extend(LIGHT_GRAY_BACKGROUND)
                    formatted_workspaces_bytes.extend(b" ")
                    formatted_workspaces_bytes.extend(workspace["name"].encode("utf-8"))
                    formatted_workspaces_bytes.extend(b" ")
                    formatted_workspaces_bytes.extend(NOT_BOLD)
                    if focused or i % 2 == 0:
                        formatted_workspaces_bytes.extend(BLACK_FOREGROUND)
                        formatted_workspaces_bytes.extend(WHITE_BACKGROUND)
                    else:
                        formatted_workspaces_bytes.extend(WHITE_BACKGROUND)
            case BarEventType.CLOCK_UPDATE:
                current_datetime = datetime.datetime.fromtimestamp(bar_event.payload)
                formatted_datetime = f" {current_datetime:%A %B %d %H:%M:%S} "
                formatted_datetime_width = wcwidth.wcswidth(formatted_datetime)
                formatted_datetime_bytes = formatted_datetime.encode("utf-8")
            case BarEventType.RESIZE:
                ...
        if bar_event.event_type.is_media_player_event():
            last_shown_media_player = media_player_to_show
            media_player_to_show = (
                min(
                    media_players.values(),
                    key=lambda payload: (
                        PLAYBACK_STATUS_PRIORITY[payload["playback_status"]],
                        payload["dbus_name"],
                    ),
                )
                if media_players
                else None
            )
            if (
                last_shown_media_player == media_player_to_show
                and media_player_to_show != event_media_player
            ):
                # if the shown media player didn't change and the update is for
                # a hidden media player than we don't need to do anything.
                continue
            if media_player_to_show is None:
                formatted_media_player = formatted_media_player_width = (
                    formatted_media_player_bytes
                ) = None
            else:
                artist = media_player_to_show["track_artist"]
                if artist:
                    artist = "/".join(artist)
                formatted_artist = f" {SEPARATOR} {artist}" if artist else ""
                title = media_player_to_show["track_title"]
                formatted_title = f" {SEPARATOR} {title}" if title else ""
                formatted_current_second = format_second_duration(
                    media_player_to_show["track_current_second"]
                )
                formatted_length_seconds = format_second_duration(
                    media_player_to_show["track_length_seconds"]
                )
                formatted_playback_status = PLAYBACK_STATUS_SPECIFIER[
                    media_player_to_show["playback_status"]
                ]
                loop_status = media_player_to_show["loop_status"].lower()
                formatted_loop_status = (
                    f" {SEPARATOR} 󰑖  {loop_status}" if loop_status != "none" else ""
                )
                formatted_media_player = f" {formatted_playback_status}  {formatted_current_second} / {formatted_length_seconds}{formatted_loop_status}{formatted_artist}{formatted_title} "
                formatted_media_player_width = wcwidth.wcswidth(formatted_media_player)
                formatted_media_player_bytes = formatted_media_player.encode("utf-8")
        current_column = 1
        writer.write(BEGIN_SYNCHRONIZED_UPDATE)
        writer.write(WHITE_BACKGROUND)
        jump_to_column(current_column)
        writer.write(CLEAR_LINE)
        try:
            if (
                formatted_datetime_bytes is not None
                and formatted_datetime_width <= terminal_width
            ):
                writer.write(formatted_datetime_bytes)
                current_column += formatted_datetime_width
                if current_column > terminal_width:
                    # no room for separator
                    raise IndexError()
            if (
                formatted_workspaces_bytes is not None
                and (current_column + formatted_workspaces_width + 1)
                <= terminal_width + 1
            ):
                writer.write(SEPARATOR_BYTES)
                current_column += 1
                writer.write(formatted_workspaces_bytes)
                current_column += formatted_workspaces_width
                if current_column > terminal_width:
                    # no room for separator
                    raise IndexError()
            if formatted_media_player_bytes is not None:
                current_column += 1  # leave room for either '│', '├' or '╞'
                media_player_start_column = terminal_width - (
                    formatted_media_player_width - 1
                )
                if media_player_start_column < current_column:
                    writer.write(SEPARATOR_BYTES)
                    raise IndexError()
                progress_bar_width = (media_player_start_column - current_column) + 1
                room_for_progress_bar = progress_bar_width > 4
                if room_for_progress_bar:
                    current_second = media_player_to_show["track_current_second"]
                    length_seconds = media_player_to_show["track_length_seconds"]
                    progress = (
                        (current_second / length_seconds) if length_seconds else 1
                    )
                    progress_width = min(
                        progress_bar_width, round(progress_bar_width * progress)
                    )
                    empty_bar = progress_width == 0
                    full_bar = progress_width == progress_bar_width
                    if empty_bar:
                        writer.write(GRAY_FOREGROUND)
                    writer.write(
                        VERTICAL_DOUBLE_RIGHT_BYTES
                        if progress_width
                        else VERTICAL_SINGLE_RIGHT_BYTES
                    )
                    double_horizontal_width = clamp(
                        progress_width - 1, 0, progress_bar_width - 2
                    )
                    writer.write(DOUBLE_HORIZONTAL_BYTES * double_horizontal_width)
                    single_horizontal_width = (
                        progress_bar_width - 2
                    ) - double_horizontal_width
                    if not empty_bar and not full_bar:
                        writer.write(GRAY_FOREGROUND)
                    writer.write(SINGLE_HORIZONTAL_BYTES * single_horizontal_width)
                    writer.write(
                        VERTICAL_DOUBLE_LEFT_BYTES
                        if progress_width == progress_bar_width
                        else VERTICAL_SINGLE_LEFT_BYTES
                    )
                    if not full_bar:
                        writer.write(BLACK_FOREGROUND)
                else:
                    writer.write(SEPARATOR_BYTES)
                jump_to_column(media_player_start_column)
                writer.write(formatted_media_player_bytes)
            else:
                writer.write(SEPARATOR_BYTES)
        except IndexError:
            ...
        finally:
            writer.write(END_SYNCHRONIZED_UPDATE)
        await writer.drain()


async def main():
    bar_event_queue = asyncio.Queue()
    async with asyncio.TaskGroup() as task_group:
        task_group.create_task(update_bar_forever(bar_event_queue))
        task_group.create_task(
            watch_all_media_players_forever(task_group, bar_event_queue)
        )
        task_group.create_task(watch_sway_forever(bar_event_queue))
        task_group.create_task(run_clock_forever(bar_event_queue))


try:
    asyncio.run(main())
except KeyboardInterrupt:
    ...
