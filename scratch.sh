name: Clone Repository Metadata

on:
  workflow_dispatch:

jobs:
  clone-metadata:
    runs-on: ubuntu-latest
    steps:
      - name: Clone repository metadata only
        run: git clone --no-checkout https://${{ secrets.GITHUB_TOKEN }}@gh.foo.com/owner/my-repo
