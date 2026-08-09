const fs = require("fs");
const path = require("path");
const matter = require("gray-matter");

// Walks src/books/ and src/articles/ directly (rather than going through
// Eleventy's collection API) so this data is available before any template
// renders and isn't affected by collection build order.
function walkMarkdownFiles(dir) {
  let results = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      results = results.concat(walkMarkdownFiles(full));
    } else if (entry.isFile() && entry.name.endsWith(".md")) {
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
  const readHours = Math.floor(totalReadMinutes / 60);
  const readMinutes = totalReadMinutes % 60;

  const topicsData = matter(
    fs.readFileSync(path.join(root, "_data", "topics.md"), "utf8")
  ).data;
  const totalTopics = (topicsData.topics || []).length;

  return {
    totalWords,
    totalWordsFormatted: totalWords.toLocaleString("en-AU"),
    totalReadTime: readHours > 0
      ? `${readHours} hour${readHours === 1 ? "" : "s"}${readMinutes ? ` ${readMinutes} min` : ""}`
      : `${readMinutes} min`,
    totalTopics
  };
};
