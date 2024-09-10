// ==UserScript==
// @name Adds scrolling JS that can be used within QB to do smarter scrolling
// @qute-js-world jseval
// @run-at document-start
// ==/UserScript==
unsafeWindow.scrollHelper = ((maxSearchDepth) => {
    const scrollableElemOverflowTypes = [
        'auto',
        'scroll',
    ]

    const getFocusedWindow = (nextElem) => {
        if (nextElem === null) return null
        if (nextElem === undefined) return getFocusedWindow(window.document.activeElement ?? null)
        const contentDocument = nextElem.shadowRoot?.activeElement?.contentDocument ?? nextElem.contentDocument
        return getFocusedWindow(contentDocument?.activeElement ?? null) ?? nextElem.ownerDocument?.defaultView ?? null
    }


    const getElementVisibleArea = (element) => element.clientHeight * element.clientWidth
    const getWindowVisibleArea = ({ document: { documentElement } }) => getElementVisibleArea(documentElement)

    const getElementScrollMaxY = (element) => element.scrollHeight - element.clientHeight
    const isElementVertScrollable = (element) => getElementScrollMaxY(element) !== 0 &&
          element.clientHeight !== 0 &&
          scrollableElemOverflowTypes.includes(getComputedStyle(element).overflowY)

    const isElement = (maybeElement) => maybeElement?.nodeType === 1

    const getElements = (element, depthRemaining) => {
        if (depthRemaining <= 0 || !isElement(element))
            return []

        const children = [].concat(
            element.contentDocument?.documentElement ?? [],
            Array.from(element.shadowRoot?.children ?? []),
            Array.from(element.children),
        )

        return children
            .flatMap((element) => getElements(element, depthRemaining - 1))
            .concat(element)
    }

    const checkElementRemainingSpace = (delta, element) =>
          (delta < 0 && element.scrollTop > 0) ||
          (delta > 0 && element.scrollTop < getScrollTopMax(element)) ||
          (delta === 0 && getScrollTopMax(element) > 0)

    const checkWindowRemainingSpace = (delta, window) => checkElementRemainingSpace(
        delta,
        window.document.scrollingElement || getDocumentBody(window.document)
    )

    const findVertScrollableChild = (delta, element) => {
        const scrollableChildren = getElements(element, maxSearchDepth + 1)
              .filter(isElementVertScrollable)
              .sort((x, y) => getElementVisibleArea(y) - getElementVisibleArea(x))

        return scrollableChildren.find((child) => checkElementRemainingSpace(delta, child)) ?? null
    }

    const findVertScrollableWindow = (delta) => {
        const focusedWindow = getFocusedWindow()
        if (focusedWindow && checkWindowRemainingSpace(delta, focusedWindow))
            return focusedWindow

        if (focusedWindow) {
            const frames = Array
                  .from(focusedWindow.frames)
                  .sort((x, y) => getWindowVisibleArea(y) - getWindowVisibleArea(x))

            const scrollableFrame = frames.find((frame) => checkWindowRemainingSpace(delta, frame))
            if (scrollableFrame) return scrollableFrame
        }

        const frames = Array
            .from(window.frames || [])
            .sort((x, y) => getWindowVisibleArea(y) - getWindowVisibleArea(x))

        return frames.find((frame) => checkWindowRemainingSpace(delta, frame))
    }

    const getScrollTopMax = (elem) => elem.scrollHeight - elem.clientHeight

    const findVertScrollableAncestor = (delta, nextElem) => {
        if (nextElem === null)
            return null

        if (isElementVertScrollable(nextElem) && checkElementRemainingSpace(delta, nextElem))
            return nextElem

        return nextElem?.parentNode
            ? findVertScrollableAncestor(delta, getParentIfNotElement(nextElem.parentNode))
            : null
    }

    const getSelectionElem = () => {
        const selection = getFocusedWindow().getSelection()
        return selection.rangeCount !== 0
            ? selection.getRangeAt(0).startContainer.parentElement
            : null
    }

    const getParentIfNotElement = (maybeElement) => {
        if (!maybeElement)
            return null

        return isElement(maybeElement)
            ? maybeElement
            : getParentIfNotElement(maybeElement.parentNode)
    }

    const getDocumentBody = (doc) => doc.body || doc.getElementsByTagName('body')[0] || doc.documentElement

    const findVertScrollable = (delta = 0) => {
        const selectionElem = getSelectionElem()
        if (selectionElem !== null) {
            const selectionScrollableElem = findVertScrollableAncestor(delta, selectionElem)
            if (selectionScrollableElem !== null)
                return selectionScrollableElem
        }

        const scrollableWindow = findVertScrollableWindow(delta)
        if (!scrollableWindow) {
            const mainBody = getDocumentBody(window.document)
            const scrollableElement = findVertScrollableChild(delta, mainBody)
            return scrollableElement ?? mainBody
        }

        const scrollableDoc = scrollableWindow.document
        const scrollableBody = scrollableDoc.scrollingElement || getDocumentBody(scrollableDoc)
        return findVertScrollableAncestor(delta, scrollableBody) ?? scrollableBody
    }

    return {
        scrollTo: (position) => findVertScrollable().scrollTo({top: position}),
        scrollToPercent: (percentPosition) => {
            const scrollElement = findVertScrollable()
            const paneHeight = scrollElement.scrollHeight
            scrollElement.scrollTo({top: percentPosition / 100 * paneHeight})
        },
        scrollBy: (delta) => findVertScrollable(delta).scrollBy({top: delta, behavior: 'smooth'}),
        scrollPage: (pages) => {
            const fakeDelta = pages < 0 ? -10 : 10
            const scrollElement = findVertScrollable(fakeDelta)
            const pageHeight = scrollElement.clientHeight
            scrollElement.scrollBy({top: pageHeight * pages})
        },
    }
})(10)
