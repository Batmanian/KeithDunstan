const { DateTime } = require("luxon");
const navigationPlugin = require('@11ty/eleventy-navigation')
const rssPlugin = require('@11ty/eleventy-plugin-rss')

module.exports = function(eleventyConfig) {

  eleventyConfig.setDataDeepMerge(true);

  // ── Tag filtering ──────────────────────────────────────────────────────────

  function filterTagList(tags) {
    return (tags || []).filter(tag => ["all", "nav", "post", "posts", "book", "books", "article", "articles"].indexOf(tag) === -1);
  }

  function bulletinCollection(items) {
    return (items || [])
      .filter(item => {
        const inputPath = item.inputPath || '';
        return inputPath.includes('src/bulletin/') || inputPath.includes('src/articles/bulletin/');
      })
      .sort((a, b) => (b.date || 0) - (a.date || 0));
  }

  eleventyConfig.addFilter("filterTagList", filterTagList)
  eleventyConfig.addFilter("bulletinCollection", bulletinCollection)

  // ── Netlify redirects (e.g. /keyword/* -> /topic/*) ────────────────────────
  // _redirects lives at the repo root; Netlify only reads it from the publish
  // directory, so it has to be passed through into the build output.
  eleventyConfig.addPassthroughCopy("_redirects");

  // ── Tag list (sorted by frequency, used for /topic/ pages) ─────────────────

  eleventyConfig.addCollection("tagList", collection => {
    const tagsObject = {}
    collection.getAll().forEach(item => {
      if (!item.data.tags) return;
      item.data.tags
        .filter(tag => !['post', 'all', 'book', 'books', 'article', 'articles'].includes(tag))
        .forEach(tag => {
          if (typeof tagsObject[tag] === 'undefined') {
            tagsObject[tag] = 1
          } else {
            tagsObject[tag] += 1
          }
        });
    });

    const tagList = []
    Object.keys(tagsObject).forEach(tag => {
      tagList.push({ tagName: tag, tagCount: tagsObject[tag] })
    })
    return tagList.sort((a, b) => b.tagCount - a.tagCount)
  });

  // ── Books collection ───────────────────────────────────────────────────────
  // All markdown files under src/books/, sorted by date ascending
  // (preserves chapter order within a book when dates match)

  eleventyConfig.addCollection("books", collection => {
    return collection
      .getFilteredByGlob("src/books/**/*.md")
      .sort((a, b) => a.date - b.date);
  });

  // ── Articles collection ────────────────────────────────────────────────────
  // All markdown files under src/articles/, sorted by date descending
  // (newest articles first)

  eleventyConfig.addCollection("articles", collection => {
    return collection
      .getFilteredByGlob("src/articles/**/*.md")
      .sort((a, b) => b.date - a.date);
  });

  // ── Per-publication article collections ───────────────────────────────────
  // Useful for publication-specific index pages and sidebar snippets

  eleventyConfig.addCollection("bulletin", collection => {
    return bulletinCollection(collection.getAll());
  });

  eleventyConfig.addCollection("walkabout", collection => {
    return collection
      .getFilteredByGlob("src/articles/walkabout-magazine/**/*.md")
      .sort((a, b) => b.date - a.date);
  });

  eleventyConfig.addCollection("australianGourmet", collection => {
    return collection
      .getFilteredByGlob("src/articles/the-australian-gourmet/**/*.md")
      .sort((a, b) => b.date - a.date);
  });

  // ── Watching and build ─────────────────────────────────────────────────────

  eleventyConfig.addWatchTarget("./src/scss/");
  eleventyConfig.setBrowserSyncConfig({
    reloadDelay: 400
  });

  // ── Date filters ───────────────────────────────────────────────────────────

  eleventyConfig.addFilter("readableDate", dateObj => {
    return DateTime.fromJSDate(dateObj, {
      zone: 'utc'
    }).toFormat("dd LLL yyyy");
  });

  eleventyConfig.addFilter('htmlDateString', (dateObj) => {
    return DateTime.fromJSDate(dateObj, {
      zone: 'utc'
    }).toFormat('yyyy-LL-dd');
  });

  return {
    dir: {
      input: "src",
      output: "dev"
    }
  };

};
