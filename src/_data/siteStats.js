const fs = require("fs");
const path = require("path");
const matter = require("gray-matter");

// Walks src/books/ and src/articles/ directly (rather than going through
// Eleventy's collection API) so this data is available before any template
// renders and isn't affected by collection build order.
//
// Content here is symlinked in from vault/ (see link-vault-content.js), so
// type checks must follow the link via fs.statSync — Dirent.isDirectory()/
// isFile() report the symlink itself, not its target, and would silently
// skip every linked file.
function walkMarkdownFiles(dir) {
  let results = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    const stat = fs.statSync(full);
    if (stat.isDirectory()) {
      results = results.concat(walkMarkdownFiles(full));
    } else if (stat.isFile() && (entry.name.endsWith(".md") || entry.name.endsWith(".njk"))) {
      results.push(full);
    }
  }
  return results;
}

function countWords(markdownBody) {
  const stripped = markdownBody
    .replace(/<[^>]*>/g, " ")
    .replace(/[#*_>`~-]/g, " ")
    .replace(/\[([^\]]*)\]\([^)]*\)/g, "$1");
  return stripped.split(/\s+/).filter(Boolean).length;
}

module.exports = () => {
  const root = path.join(__dirname, "..");
  let totalWords = 0;

  for (const dir of ["books", "articles"]) {
    for (const file of walkMarkdownFiles(path.join(root, dir))) {
      const raw = fs.readFileSync(file, "utf8");
      const { content } = matter(raw);
      totalWords += countWords(content);
    }
  }

  const WORDS_PER_MINUTE = 200;
  const totalReadMinutes = Math.round(totalWords / WORDS_PER_MINUTE);
  const readHours = Math.round(totalReadMinutes / 60);

  const EXCLUDED_TAGS = new Set(["all", "nav", "post", "posts", "book", "books", "article", "articles"]);
  const uniqueTags = new Set();
  let totalArticles = 0;
  for (const dir of ["books", "articles"]) {
    for (const file of walkMarkdownFiles(path.join(root, dir))) {
      const raw = fs.readFileSync(file, "utf8");
      const { data } = matter(raw);
      for (const tag of (data.tags || [])) {
        if (!EXCLUDED_TAGS.has(tag)) uniqueTags.add(tag);
      }
      if (dir === "articles" && !data.eleventyExcludeFromCollections) {
        totalArticles++;
      }
    }
  }
  const totalTopics = uniqueTags.size;

  // Estimated total words in Keith's full published output — see methodology in todo.md §15.
  // Sun News-Pictorial column (1946–1978, 5 days/week, ~300 words): ~2,400,000
  // The Bulletin column (~1,950 articles, ~700 words each):         ~1,365,000
  // Books (~30 titles, ~65,000 words each):                         ~1,950,000
  // Other journalism (The Age, Walkabout, Gourmet, etc.):             ~285,000
  // Total:                                                          ~6,000,000
  const estimatedTotalWords = 6000000;
  const percentTranscribed = Math.round((totalWords / estimatedTotalWords) * 100);

  return {
    totalWords,
    totalWordsFormatted: totalWords.toLocaleString("en-AU"),
    totalReadTime: readHours > 0
      ? `${readHours} hour${readHours === 1 ? "" : "s"}`
      : `${totalReadMinutes} min`,
    totalTopics,
    totalArticles: totalArticles.toLocaleString("en-AU"),
    percentTranscribed: `~${percentTranscribed}%`,
  };
};
