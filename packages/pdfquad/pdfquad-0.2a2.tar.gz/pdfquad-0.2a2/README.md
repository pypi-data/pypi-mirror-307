# PDF QUality Assessment for Digitisation batches

## What is pdfquad?

Pdfquad is a simple tool for automated quality assessment of PDF documents in digitisation batches against a user-defined technical profile. It uses [PyMuPDF](https://pymupdf.readthedocs.io/) to parse the PDF file structure and extract some relevant properties. Properties of embedded images are extracted using [Pillow](https://pillow.readthedocs.io/).

These properties are serialized to a simple XML structure, which is then evaluated against [Schematron rules](http://en.wikipedia.org/wiki/Schematron) that define the expected/required technical characteristics.

## Installation

Install the software with the [pip package manager](https://en.wikipedia.org/wiki/Pip_(package_manager)):

```
pip install pdfquad
```

Then run pdfquad once:

```
pdfquad
```

Depending on your system, pdfquad will create a folder named `pdfquad` in one of the following locations: 

- For Linux, it will use the location defined by environment variable `$XDG_CONFIG_HOME`. If this variable is not set, it will use the `.config` directory in the user's home folder (e.g. `/home/johan/.config/pdfquad`). Note that the `.config` directory is hidden by default.
- For Windows, it will use the `AppData\Local` folder (e.g. `C:\Users\johan\AppData\Local\pdfquad`).

The folder contains two subdirectories named `profiles` and `schemas`, which is explained below.

## Profiles directory

A profile is an XML file that defines how a digitisation batch is evaluated. It is made up of one or more `schema` elements, that each link a file or directory naming pattern to a Schematron file. Here's an example:

```xml
<?xml version="1.0"?>

<profile>

<schema type="parentDirName" match="endswith" pattern="pi-85">pdf-dbnl-85.sch</schema>
<schema type="parentDirName" match="endswith" pattern="pi-50">pdf-dbnl-50.sch</schema>

</profile>
```

Here we see two `schema` elements. Each element refers to a Schematron file (explained in the next section). The values of the `type`, `match` and `pattern` attributes define how this file is linked to file or directory names inside the batch:

- If **type** is "fileName", the matching is based on the naming of a PDF. In case of "parentDirName" the matching uses the naming of the direct parent directory of a PDF.
- The **match** attribute defines whether the matching pattern with the file or directory name is exact ("is") or partial ("startswith", "endswith", "contains".)
- The **pattern** attribute defines a text string that is used for the match.

In the example above, the profile says that if a PDF has a direct parent directory whose name ends with "pi-85", pdfquad should use Schematron file "pdf-dbnl-85.sch". If the directory name ends with "pi-50", it should use "pdf-dbnl-50.sch".

## Available profiles

Currently the following profiles are included:

|Profile|Description|
|:--|:--|
|dbnl-fulltext.xml|Profile for DBNL fulltext digitization batches|

## Schemas directory

The directory contains Schematron files that define the rules on which the quality assessment is based. Some background information about this type of rule-based validation can be found in [this blog post](https://www.bitsgalore.org/2012/09/04/automated-assessment-jp2-against-technical-profile).

## Available schemas

Currently the following schemas are included:

|Schema|Description|
|:--|:--|
|pdf-dbnl-50.sch|Schema for small access PDFs with 50% quality JPEG compression.|
|pdf-dbnl-85.sch|Schema for production master PDFs  with 85% quality JPEG compression.|

## Command-line syntax

The general syntax of pdfquad is:

```
usage: pdfquad [-h] [--version] {process,list} ...
```

Pdfquad has two sub-commands:

|Command|Description|
|:-----|:--|
|`process`|process a batch.|
|`list`|list available profiles and schemas.|

### process command

Run pdfquad with the `process` command to process a batch. The syntax is:

```
usage: pdfquad process [-h] [--maxpdfs MAXPDFS] [--prefixout PREFIXOUT]
                       [--outdir OUTDIR] [--verbose]
                       profile batchDir
```

The `process` command expects the following positional arguments: 

|Argument|Description|
|:-----|:--|
|`profile`|this defines the validation profile. Note that any file paths entered here will be ignored, as Pdfquad only accepts  profiles from the profiles directory. You can just enter the file name without the path. Use the `list` command to list all available profiles.|
|`batchDir`|this defines the batch directory that will be analyzed.|

In addition, the following optional arguments are available:

|Argument|Description|
|:-----|:--|
|`--maxpdfs`, `-x`|this defines the maximum number of PDFs that are reported in each output XML file (default: 10).|
|`--prefixout`, `p`|this defines a text prefix on which the names of the output files are based (default: "pq").|
|`--outdir`, `-o`|this defines the directory where output is written (default: current working directory from which pdfquad is launched).|
|`--verbose`, `-b`|this tells pdfquad to report Schematron output in verbose format.|

In the simplest case, we can call pdfquad with the profile and the batch directory as the only arguments:

```
pdfquad process dbnl-fulltext.xml ./mybatch
```

Pdfquad will now recursively traverse all directories and files inside the "mybatch" directory, and analyse all PDF files (based on a file extension match).

### list command

Run pdfquad with the `list` command to get a list of the available profiles and schemas, as well as their locations. For example:

```
pdfquad list
```

Results in:

```
Available profiles (directory /home/johan/.config/pdfquad/profiles):
  - dbnl-fulltext.xml
Available schemas (directory /home/johan/.config/pdfquad/schemas):
  - pdf-dbnl-85.sch
  - pdf-dbnl-50.sch
```

## Output

Pdfquad reports the following output:

### Comprehensive output file (XML)

Pdfquad generates one or more comprehensive output files in XML format. For each PDF, these contain all extracted properties, as well a the Schematron report and the assessment status. [Here's an example file](./examples/pq_batchtest_001.xml).

Since these files can get really large, Pdfquad splits the results across multiple output files, using the following naming convention:

- pq_mybatch_001.xml
- pq_mybatch_002.xml
- etcetera

By default Pdfquad limits the number of reported PDFs for each output file to 10, after which it creates a new file. This behaviour can be changed by using the `--maxpdfs` (alias `-x`) option. For example, the command below will limit the number of PDFs per output file to 1 (so each PDF will have its dedicated output file):

```
pdfquad process dbnl-fulltext.xml ./mybatch -x 1
```

### Summary file (CSV)

This is a comma-delimited text file with, for each PDF, the assessment status, the number of pages, and a reference to its corresponding comprehensive output file. As an example:

``` csv
file,status,noPages,fileOut
/home/johan/test-batches/mybatch/20241106/anbe001lexi02/300dpi-85/anbe001lexi02_01.pdf,pass,1528,/home/johan/test-batches/pq_mybatch_001.xml
/home/johan/test-batches/mybatch/20241106/anbe001lexi02/300dpi-50/anbe001lexi02_01.pdf,fail,1528,/home/johan/test-batches/pq_mybatch_001.xml
/home/johan/test-batches/mybatch/20241106/brin003196603/300dpi-85/brin003196603_01.pdf,fail,1260,/home/johan/test-batches/pq_mybatch_001.xml
/home/johan/test-batches/mybatch/20241106/brin003196603/300dpi-50/brin003196603_01.pdf,fail,1260,/home/johan/test-batches/pq_mybatch_001.xml
/home/johan/test-batches/mybatch/20241105/_deu002201201/300dpi-85/_deu002201201_01.pdf,fail,297,/home/johan/test-batches/pq_mybatch_001.xml
/home/johan/test-batches/mybatch/20241105/_deu002201201/300dpi-50/_deu002201201_01.pdf,fail,297,/home/johan/test-batches/pq_mybatch_001.xml
/home/johan/test-batches/mybatch/20241105/_boe012192401/300dpi-85/_boe012192401_01.pdf,pass,346,/home/johan/test-batches/pq_mybatch_001.xml
/home/johan/test-batches/mybatch/20241105/_boe012192401/300dpi-50/_boe012192401_01.pdf,fail,346,/home/johan/test-batches/pq_mybatch_001.xml
```

## Licensing

Pdfquad is released under the [Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0).

## Useful links

- [Schematron](http://en.wikipedia.org/wiki/Schematron)


