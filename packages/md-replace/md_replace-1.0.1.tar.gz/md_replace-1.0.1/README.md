
# md_replace

A simple command-line tool to replace file paths in markdown files with the actual file contents.  This is particularly useful for managing large prompts for Large Language Models (LLMs) where you need to include code snippets or extensive documentation.

## Features

- Replaces file paths enclosed in double curly braces `{{filepath}}` with the content of the specified file.  Supports relative paths.
- Handles `.md` files recursively within the current directory.
- Creates new files with a specified suffix to avoid overwriting originals.
- Cross-platform compatibility (Windows, Linux, macOS).
- Installable via pip.

## Installation

```bash
pip install md_replace
```

## Usage

```bash
md_replace <suffix>
```

- `<suffix>`: The suffix to be appended to the new markdown files. For example, if the suffix is `_replaced`, `example.md` will be processed and saved as `example_replaced.md`.

## Example

Let's say you have a markdown file `prompt.md` with the following content:

```markdown
My prompt:

{{code.py}}

More text...

{{docs/design.md}}
```

Running `md_replace _processed` will create a new file `prompt_processed.md` where the file paths are replaced with the contents of `code.py` and `docs/design.md`.

## Motivation and Comparison with Jinja2

This tool was created to streamline the process of managing long prompts for LLMs, specifically focusing on directly embedding file content into markdown files. While Jinja2 provides powerful templating capabilities, it often introduces complexities that are not necessary for this specific use case.  `md_replace` prioritizes simplicity and ease of use, targeting the direct replacement of file paths with content without requiring familiarity with templating engines.  Furthermore,  using Jinja2 would require loading the entire files into memory to render the template whereas `md_replace` opens and processes the files individually, making it more memory-efficient for extremely large files.


---

# md_replace

Markdownファイル内のファイルパスを実際のファイル内容に置換するシンプルなコマンドラインツールです。  これは、コードスニペットや大規模なドキュメントを含める必要のある大規模言語モデル（LLM）のプロンプトを管理するのに特に役立ちます。

## 機能

- ダブルカーリーブレース `{{ファイルパス}}` で囲まれたファイルパスを、指定されたファイルの内容に置き換えます。相対パスをサポートします。
- 現在のディレクトリ内の `.md` ファイルを再帰的に処理します。
- 元のファイルを上書きしないように、指定されたサフィックスで新しいファイルを作成します。
- クロスプラットフォーム互換性（Windows、Linux、macOS）。
- pip 経由でインストールできます。

## インストール

```bash
pip install md_replace
```

## 使い方

```bash
md_replace <サフィックス>
```

- `<サフィックス>`: 新しいMarkdownファイルに追加されるサフィックスです。たとえば、サフィックスが `_replaced` の場合、`example.md` は処理され、`example_replaced.md` として保存されます。

## 例

`prompt.md` というMarkdownファイルに次の内容があるとします。

```markdown
私のプロンプト：

{{code.py}}

さらにテキスト...

{{docs/design.md}}
```

`md_replace _processed` を実行すると、`code.py` と `docs/design.md` の内容でファイルパスが置き換えられた新しいファイル `prompt_processed.md` が作成されます。

## Jinja2との比較と動機

このツールは、LLMの長いプロンプトを管理するプロセスを合理化するために作成されました。特に、ファイルの内容をMarkdownファイルに直接埋め込むことに焦点を当てています。Jinja2は強力なテンプレート機能を提供しますが、この特定のユースケースには必要のない複雑さを伴うことがよくあります。 `md_replace` はシンプルさと使いやすさを優先し、テンプレートエンジンに精通していなくても、ファイルパスをコンテンツに直接置き換えることを目的としています。 さらに、Jinja2 を使用するには、テンプレートをレンダリングするためにファイル全体をメモリにロードする必要がありますが、`md_replace` はファイルを個別に開いて処理するため、非常に大きなファイルに対してメモリ効率が高くなります。