# Hardhik's GitHub profile

This folder contains the source for the special profile repository \`hardhik00007\`.

## Files

\`\`\`text
hardhik00007/
├── README.md
├── SETUP.md
├── assets/
│   ├── profile-banner.jpg
│   ├── project-aqshield.svg
│   ├── project-variable.svg
│   ├── project-quantum.svg
│   ├── project-idea-incubator.svg
│   ├── profile-stats.svg
│   └── languages.svg
├── scripts/
│   └── update_profile_stats.py
└── .github/workflows/
    └── update-profile-stats.yml
\`\`\`

## What changed

- The header is now an illustrated coding-desk scene. It borrows the reference's Japanese screen-print / packaging-art language without depicting a keyboard switch or sushi product.
- Each featured project has its own locally stored illustration.
- The broken \`github-readme-stats.vercel.app\` and \`github-readme-activity-graph.vercel.app\` embeds have been removed.
- Local stats and language SVGs are stored in this repository. A GitHub Actions workflow refreshes them weekly and can also be run manually from the Actions tab.
- The streak card remains a separate hosted image. The full GitHub contribution calendar is available in the native Activity section on the profile page.

## Update the profile

Edit \`README.md\` to change the introduction, projects, technology list, or links. Replace \`assets/profile-banner.jpg\` to change the banner, or update the four project SVGs to change the project artwork.

To refresh the stats manually, open the profile repository's **Actions** tab, select **Refresh profile statistics**, and choose **Run workflow**. The workflow needs \`contents: write\` permission for its built-in GitHub token. The YAML in this package already declares that permission; repository Actions settings must allow the workflow token to write to the repository.

The language card reports GitHub's primary-language label per public repository. It is not a measure of skill or exact byte share. Stats are refreshed weekly rather than on every profile visit.

## Local editing

\`\`\`bash
git clone https://github.com/hardhik00007/hardhik00007.git
cd hardhik00007
# edit README.md or assets/
git add README.md assets scripts .github/workflows
git commit -m "Update GitHub profile"
git push
\`\`\`

The email link in the README is public. Remove it if you do not want the address visible to everyone.