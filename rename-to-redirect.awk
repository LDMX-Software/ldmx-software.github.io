# pipe result of git status --short --porcelain here to dump renames into redirects

# lines are of the form
#   <status> <file> [-> <renamed-file>]
# where the last two are only present in renamed files
# only operate on lines that are renames of src markdown files
$1 == "R" && $2 ~ /^src\/.*\.md$/ {
  gsub("src","",$2);
  gsub("src","",$4);
  gsub(".md",".html",$2);
  gsub(".md",".html",$4);
  printf "\"%s\" = \"%s\"\n", $2, $4
}
