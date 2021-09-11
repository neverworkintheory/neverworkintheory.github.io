/**
 * Find and fix bibliographic citations.
 * @param {string} toRoot Path to root of site.
 */
const fixBibCites = (toRoot) => {
  console.log('fixBibCites')
  Array.from(document.querySelectorAll('cite'))
    .forEach(node => {
      console.log(node)
      const keys = node.innerHTML
            .split(',')
            .map(key => key.trim())
            .map(key => `<a href="${toRoot}/bib/#${key}">${key}</a>`)
            .join(', ')
      const cite = document.createElement('span')
      cite.innerHTML = `[${keys}]`
      cite.classList.add('cite')
      node.parentNode.replaceChild(cite, node)
    })
}

/**
 * Find the relative path to the root directory given the page URL from the root.
 * @param {string} pageUrl Contains '/path/to/this/file.html'
 * @returns Relative path to root directory
 */
const pathToRoot = (pageUrl) => {
  const depth = pageUrl.split('/').length - 2 // Because '/a/b/c.html' => ['', 'a', 'b', 'c.html']
  return (depth === 0) ? '.' : Array(depth).fill('..').join('/')
}

/**
 * Perform all in-page fixes.
 * @param {string} toRoot Path to root of site (default is one level up).
 */
const fixPage = (pageUrl) => {
  const toRoot = pathToRoot(pageUrl)
  fixBibCites(toRoot)
}
