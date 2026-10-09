# DDI Tools Landscape

A curated, interactive landscape of tools for the DDI community. Explore and compare solutions for metadata management, survey design, data transformation, and more — all visualised using Landscape2.

This repository contains the initial version of the DDI Tools Landscape created during the EDDI25 Hackathon.

The landscape is built using [Landscape2](https://github.com/cncf/landscape2), an open-source tool for visualising and exploring technology ecosystems.

## Landscape creation steps

This landscape was created with the following steps:

1. **Install Landscape2**

   curl --proto '=https' --tlsv1.2 -LsSf https://github.com/cncf/landscape2/releases/download/v1.1.0/landscape2-installer.sh | sh

   After installation, you may need to restart your shell session.

2. **Create a new landscape directory**

   landscape2 new --output-dir ddi-tools

3. **(Optional) Sync or copy your landscape directory as needed**

   Use your preferred method (e.g., rsync, scp, or file manager) to move or back up the `ddi-tools` directory between systems.

4. **Build the landscape**

   cd ddi-tools
   landscape2 build --data-file data.yml --settings-file settings.yml --guide-file guide.yml --games-file games.yml --logos-path logos --output-dir build

5. **Serve the landscape locally**

   landscape2 serve --landscape-dir build

   The landscape will be available at http://localhost:8080 by default.

## How to run this landscape from a clone

If you have cloned this repository and want to run the landscape locally:

1. **Install Landscape2** (if not already installed)

   curl --proto '=https' --tlsv1.2 -LsSf https://github.com/cncf/landscape2/releases/download/v1.1.0/landscape2-installer.sh | sh

2. **Navigate to the project directory**

   cd ddi-tools

3. **Build the landscape**

   landscape2 build --data-file data.yml --settings-file settings.yml --guide-file guide.yml --games-file games.yml --logos-path logos --output-dir build

4. **Serve the landscape locally**

   landscape2 serve --landscape-dir build

   The landscape will be available at http://localhost:8080 by default.

## Editing tool data

Entries are maintained as one YAML file per item under `tools/`, `members/`,
`examples/` and `profiles/`, rather than directly in `data.yml`. `data.yml` and
`guide.yml` are generated and should not be edited by hand.

- `structure.yml` lists the categories and subcategories, in display order.
  An optional `guide` field on a category or subcategory is used as its
  introduction text in `guide.yml`.
- `tools/<tool>.yml` holds one tool's data: `category`, `subcategory`, and
  `order` (position within the subcategory), followed by the usual landscape2
  item fields (`name`, `homepage_url`, `description`, `extra`, etc.). A tool
  listed under more than one subcategory (e.g. EpiData Software) gets a
  separate file per placement.

To add, remove, or edit a tool, change the relevant file(s) under `tools/`
(and `structure.yml` if you're adding a new category/subcategory), then
regenerate `data.yml` and `guide.yml`:

    python3 scripts/build_data.py

Requires PyYAML (`pip install pyyaml`). Re-run the normal `landscape2 build`
step afterwards to rebuild the site.

## Publishing to GitHub Pages

`.github/workflows/deploy-pages.yml` rebuilds and publishes the landscape
automatically on every push to `main` (and can be run manually via the
Actions tab). It regenerates `data.yml` and `guide.yml`, runs
`landscape2 build`, and deploys the result with GitHub's Pages actions.

One-time repository setup: in **Settings → Pages**, set **Source** to
**GitHub Actions**.

## Notes

- Some license information has been updated or generalised.
- Some information is likely out of date but has been kept as-is for reference.
- Information under `annotations` is not directly visible in the landscape UI, but is preserved for external tools or future use.
- In some cases, multiple pieces of information were combined under the same `summary_<key>` field, as there is no perfect equivalency to the original Excel sheet.
- Some keys (e.g., `summary_release_rate`) are used for related but not exact purposes (such as listing supported DDI versions instead of release rate) to make more information visible in landscape cards.
- The guide is generated: an optional introduction per category/subcategory from `structure.yml`, plus each item's name, link and description.
- Many pictures are missing.
- Copilot Chat was leveraged to create the initial versions of files from the original Excel sheet.

## About

- **Author:** Markus Tuominen (FSD)
- **Event:** EDDI25 Hackathon
- **Tooling:** [Landscape2](https://github.com/cncf/landscape2)

## Customisation

- Edit `data.yml`, `settings.yml`, `guide.yml`, and `games.yml` to update the content and appearance of your landscape.
- Place SVG logo files in the `logos` directory.

For more information, see the [Landscape2 documentation](https://github.com/cncf/landscape2).

## License

The repository is licensed with [MIT](LICENSE), excluding files in logos directory which are not covered by the license of this repository and instead retain their original copyrights/licenses.
