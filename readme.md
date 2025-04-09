# Utility Scripts Repository

## Contents

- analyse_lint_rules.py
- file_size.py

### analyse_lint_rules.py

#### usage:

`python analyse_lint_rules.py <directory>`

This package walks every directory and subdirectory to gather all `analysis_options.yaml` files contained in the codebase.

It assumes the first found file will be the 'root' analysis options.

All children are then compared to the root for unique rules.

You can set it to delete any files that are either empty (containing no rules at all) or that contain no unique rules from the root.

As of 8/4/25 there are around 160 `analysis_options.yaml` files in the codebase with around 110 of them containing either no rules at all or no unique rules.

There are lots of very suss exclusions as well because people just love to commit garbage code to the codebase without any oversight.

This script is obviously a bit shit and needs work but it gives a pretty good idea of the scale of the problem.


### file_size.py

Not really much to explain with this one.

#### usage:

`python file_size.py <target_directory> --exclude .git,build,png,jpg,jpeg --include features,core`

Returns the top 25 largest files it finds in descending order.