/// This list represents the default file types that ripgrep ships with. In
/// general, any file format is fair game, although it should generally be
/// limited to reasonably popular open formats. For other cases, you can add
/// types to each invocation of ripgrep with the '--type-add' flag.
///
/// If you would like to add or improve this list, please file a PR:
/// <https://github.com/BurntSushi/ripgrep>.
///
/// Please try to keep this list sorted lexicographically and wrapped to 79
/// columns (inclusive).
#[rustfmt::skip]
pub(crate) const DEFAULT_TYPES: &[(&str, &[&str])] = &[
    ("agda", &["*.agda", "*.lagda"]),
    ("aidl", &["*.aidl"]),
    ("amake", &["*.mk", "*.bp"]),
    ("asciidoc", &["*.adoc", "*.asc", "*.asciidoc"]),
    ("asm", &["*.asm", "*.s", "*.S"]),
    ("asp", &[
        "*.aspx", "*.aspx.cs", "*.aspx.vb", "*.ascx", "*.ascx.cs", "*.ascx.vb",
    ]),
    ("ats", &["*.ats", "*.dats", "*.sats", "*.hats"]),
    ("avro", &["*.avdl", "*.avpr", "*.avsc"]),
    ("awk", &["*.awk"]),
    ("bazel", &[
        "*.bazel", "*.bzl", "*.BUILD", "*.bazelrc", "BUILD", "WORKSPACE",
    ]),
    ("bitbake", &["*.bb", "*.bbappend", "*.bbclass", "*.conf", "*.inc"]),
    ("brotli", &["*.br"]),
    ("buildstream", &["*.bst"]),
    ("bzip2", &["*.bz2", "*.tbz2"]),
    ("c", &["*.[chH]", "*.[chH].in", "*.cats"]),
    ("cabal", &["*.cabal"]),
    ("cbor", &["*.cbor"]),
    ("cert", &[
        // Certificate files:
        "*.crt",
        "*.cer",
        "*.ca-bundle",
        "*.p7b",
        "*.p7c",
        "*.p7s",
        // Keystore Files:
        "*.key",
        "*.keystore",
        "*.jks",
        // Combined certificate and key files:
        "*.p12",
        "*.pfx",
        "*.pem",
    ]),
    ("ceylon", &["*.ceylon"]),
    ("clojure", &["*.clj", "*.cljc", "*.cljs", "*.cljx"]),
    ("cmake", &["*.cmake", "CMakeLists.txt"]),
    ("coffeescript", &["*.coffee"]),
    ("config", &["*.cfg", "*.conf", "*.config", "*.ini"]),
    ("coq", &["*.v"]),
    ("cpp", &[
        "*.[ChH]", "*.cc", "*.[ch]pp", "*.[ch]xx", "*.hh",  "*.inl",
        "*.[ChH].in", "*.cc.in", "*.[ch]pp.in", "*.[ch]xx.in", "*.hh.in",
    ]),
    ("creole", &["*.creole"]),
    ("crystal", &["Projectfile", "*.cr", "*.ecr", "shard.yml"]),
    ("csharp", &["*.cs"]),
    ("cshtml", &["*.cshtml"]),
    ("css", &["*.css", "*.scss"]),
    ("csv", &["*.csv"]),
    ("cuda", &["*.cu", "*.cuh"]),
    ("cython", &["*.pyx", "*.pxi", "*.pxd"]),
    ("d", &["*.d"]),
    ("dart", &["*.dart"]),
    ("dhall", &["*.dhall"]),
    ("diff", &["*.patch", "*.diff"]),
    ("docker", &["*Dockerfile*"]),
    ("dvc", &["Dvcfile", "*.dvc"]),
    ("ebuild", &["*.ebuild"]),
    ("edn", &["*.edn"]),
    ("elisp", &["*.el"]),
    ("elixir", &["*.ex", "*.eex", "*.exs"]),
    ("elm", &["*.elm"]),
    ("erb", &["*.erb"]),
    ("erlang", &["*.erl", "*.hrl"]),
    ("fennel", &["*.fnl"]),
    ("fidl", &["*.fidl"]),
    ("fish", &["*.fish"]),
    ("flatbuffers", &["*.fbs"]),
    ("fortran", &[
        "*.f", "*.F", "*.f77", "*.F77", "*.pfo",
        "*.f90", "*.F90", "*.f95", "*.F95",
    ]),
    ("fsharp", &["*.fs", "*.fsx", "*.fsi"]),
    ("fut", &["*.fut"]),
    ("gap", &["*.g", "*.gap", "*.gi", "*.gd", "*.tst"]),
    ("gn", &["*.gn", "*.gni"]),
    ("go", &["*.go"]),
    ("gradle", &["*.gradle"]),
    ("groovy", &["*.groovy", "*.gradle"]),
    ("gzip", &["*.gz", "*.tgz"]),
    ("h", &["*.h", "*.hpp"]),
    ("haml", &["*.haml"]),
    ("hbs", &["*.hbs"]),
    ("hs", &["*.hs", "*.lhs"]),
    ("html", &["*.htm", "*.html", "*.ejs"]),
    ("hy", &["*.hy"]),
    ("idris", &["*.idr", "*.lidr"]),
    ("janet", &["*.janet"]),
    ("java", &["*.java", "*.jsp", "*.jspx", "*.properties"]),
    ("jinja", &["*.j2", "*.jinja", "*.jinja2"]),
    ("jl", &["*.jl"]),
    ("js", &["*.js", "*.jsx", "*.vue"]),
    ("json", &["*.json"]),
    ("jsonl", &["*.jsonl"]),
    ("jupyter", &["*.ipynb", "*.jpynb"]),
    ("k", &["*.k"]),
    ("kotlin", &["*.kt", "*.kts"]),
    ("less", &["*.less"]),
    ("license", &[
        // General
        "COPYING", "COPYING[.-]*",
        "COPYRIGHT", "COPYRIGHT[.-]*",
        "EULA", "EULA[.-]*",
        "licen[cs]e", "licen[cs]e.*",
        "LICEN[CS]E", "LICEN[CS]E[.-]*", "*[.-]LICEN[CS]E*",
        "NOTICE", "NOTICE[.-]*",
        "PATENTS", "PATENTS[.-]*",
        "UNLICEN[CS]E", "UNLICEN[CS]E[.-]*",
        // GPL (gpl.txt, etc.)
        "agpl[.-]*",
        "gpl[.-]*",
        "lgpl[.-]*",
        // Other license-specific (APACHE-2.0.txt, etc.)
        "AGPL-*[0-9]*",
        "APACHE-*[0-9]*",
        "BSD-*[0-9]*",
        "CC-BY-*",
        "GFDL-*[0-9]*",
        "GNU-*[0-9]*",
        "GPL-*[0-9]*",
        "LGPL-*[0-9]*",
        "MIT-*[0-9]*",
        "MPL-*[0-9]*",
        "OFL-*[0-9]*",
    ]),
    ("lilypond", &["*.ly", "*.ily"]),
    ("lisp", &["*.el", "*.lisp", "*.lsp", "*.sc", "*.scm"]),
    ("lock", &["*.lock", "package-lock.json", "requirements.txt", "go.sum", "pnpm-lock.yaml"]),
    ("log", &["*.log"]),
    ("lua", &["*.lua"]),
    ("lz4", &["*.lz4"]),
    ("lzma", &["*.lzma"]),
    ("m4", &["*.ac", "*.m4"]),
    ("make", &[
        "[Gg][Nn][Uu]makefile", "[Mm]akefile",
        "[Gg][Nn][Uu]makefile.am", "[Mm]akefile.am",
        "[Gg][Nn][Uu]makefile.in", "[Mm]akefile.in",
        "*.mk", "*.mak"
    ]),
    ("mako", &["*.mako", "*.mao"]),
    ("man", &["*.[0-9lnpx]", "*.[0-9][cEFMmpSx]"]),
    ("matlab", &["*.m"]),
    ("md", &["*.markdown", "*.md", "*.mdown", "*.mkdn"]),
    ("meson", &["meson.build", "meson_options.txt"]),
    ("minified", &["*.min.html", "*.min.css", "*.min.js"]),
    ("mint", &["*.mint"]),
    ("mk", &["mkfile"]),
    ("ml", &["*.ml"]),
    ("msbuild", &[
        "*.csproj", "*.fsproj", "*.vcxproj", "*.proj", "*.props", "*.targets",
    ]),
    ("nim", &["*.nim", "*.nimf", "*.nimble", "*.nims"]),
    ("nix", &["*.nix"]),
    ("objc", &["*.h", "*.m"]),
    ("objcpp", &["*.h", "*.mm"]),
    ("ocaml", &["*.ml", "*.mli", "*.mll", "*.mly"]),
    ("org", &["*.org", "*.org_archive"]),
    ("pascal", &["*.pas", "*.dpr", "*.lpr", "*.pp", "*.inc"]),
    ("pdf", &["*.pdf"]),
    ("perl", &["*.perl", "*.pl", "*.PL", "*.plh", "*.plx", "*.pm", "*.t"]),
    ("php", &["*.php", "*.php3", "*.php4", "*.php5", "*.phtml"]),
    ("po", &["*.po"]),
    ("pod", &["*.pod"]),
    ("postscript", &["*.eps", "*.ps"]),
    ("protobuf", &["*.proto"]),
    ("ps", &["*.cdxml", "*.ps1", "*.ps1xml", "*.psd1", "*.psm1"]),
    ("puppet", &["*.erb", "*.pp", "*.rb"]),
    ("purs", &["*.purs"]),
    ("py", &[
        "*.py",
        "*.pyi",
        // From a spell-check perspective, this is more like Python than toml
        "pyproject.toml",
    ]),
    ("qmake", &["*.pro", "*.pri", "*.prf"]),
    ("qml", &["*.qml"]),
    ("r", &["*.R", "*.r", "*.Rmd", "*.Rnw"]),
    ("racket", &["*.rkt"]),
    ("rdoc", &["*.rdoc"]),
    ("readme", &["README*", "*README"]),
    ("red", &["*.r", "*.red", "*.reds"]),
    ("robot", &["*.robot"]),
    ("rst", &["*.rst"]),
    ("ruby", &[
        // Idiomatic files
        "config.ru", "Gemfile", ".irbrc", "Rakefile",
        // Extensions
        "*.gemspec", "*.rb", "*.rbw"
    ]),
    ("rust", &[
        "*.rs",
        // From a spell-check perspective, this is more like Python than toml
        "Cargo.toml",
    ]),
    ("sass", &["*.sass", "*.scss"]),
    ("scala", &["*.scala", "*.sbt"]),
    ("sh", &[
        // Portable/misc. init files
        ".login", ".logout", ".profile", "profile",
        // bash-specific init files
        ".bash_login", "bash_login",
        ".bash_logout", "bash_logout",
        ".bash_profile", "bash_profile",
        ".bashrc", "bashrc", "*.bashrc",
        // csh-specific init files
        ".cshrc", "*.cshrc",
        // ksh-specific init files
        ".kshrc", "*.kshrc",
        // tcsh-specific init files
        ".tcshrc",
        // zsh-specific init files
        ".zshenv", "zshenv",
        ".zlogin", "zlogin",
        ".zlogout", "zlogout",
        ".zprofile", "zprofile",
        ".zshrc", "zshrc",
        // Extensions
        "*.bash", "*.csh", "*.ksh", "*.sh", "*.tcsh", "*.zsh",
    ]),
    ("slim", &["*.skim", "*.slim", "*.slime"]),
    ("smarty", &["*.tpl"]),
    ("sml", &["*.sml", "*.sig"]),
    ("soy", &["*.soy"]),
    ("spark", &["*.spark"]),
    ("spec", &["*.spec"]),
    ("sql", &["*.sql", "*.psql"]),
    ("stylus", &["*.styl"]),
    ("sv", &["*.v", "*.vg", "*.sv", "*.svh", "*.h"]),
    ("svg", &["*.svg"]),
    ("swift", &["*.swift"]),
    ("swig", &["*.def", "*.i"]),
    ("systemd", &[
        "*.automount", "*.conf", "*.device", "*.link", "*.mount", "*.path",
        "*.scope", "*.service", "*.slice", "*.socket", "*.swap", "*.target",
        "*.timer",
    ]),
    ("taskpaper", &["*.taskpaper"]),
    ("tcl", &["*.tcl"]),
    ("tex", &["*.tex", "*.ltx", "*.cls", "*.sty", "*.bib", "*.dtx", "*.ins"]),
    ("texinfo", &["*.texi"]),
    ("textile", &["*.textile"]),
    ("tf", &["*.tf"]),
    ("thrift", &["*.thrift"]),
    ("toml", &["*.toml"]),
    ("ts", &["*.ts", "*.tsx"]),
    ("twig", &["*.twig"]),
    ("txt", &["*.txt"]),
    ("typoscript", &["*.typoscript"]),
    ("vala", &["*.vala"]),
    ("vb", &["*.vb"]),
    ("vcl", &["*.vcl"]),
    ("verilog", &["*.v", "*.vh", "*.sv", "*.svh"]),
    ("vhdl", &["*.vhd", "*.vhdl"]),
    ("vimscript", &[
        "*.vim", ".vimrc", ".gvimrc", "vimrc", "gvimrc", "_vimrc", "_gvimrc",
    ]),
    ("webidl", &["*.idl", "*.webidl", "*.widl"]),
    ("wiki", &["*.mediawiki", "*.wiki"]),
    ("xml", &[
        "*.xml", "*.xml.dist", "*.dtd", "*.xsl", "*.xslt", "*.xsd", "*.xjb",
        "*.rng", "*.sch", "*.xhtml",
    ]),
    ("xz", &["*.xz", "*.txz"]),
    ("yacc", &["*.y"]),
    ("yaml", &["*.yaml", "*.yml"]),
    ("yang", &["*.yang"]),
    ("z", &["*.Z"]),
    ("zig", &["*.zig"]),
    ("zsh", &[
        ".zshenv", "zshenv",
        ".zlogin", "zlogin",
        ".zlogout", "zlogout",
        ".zprofile", "zprofile",
        ".zshrc", "zshrc",
        "*.zsh",
    ]),
    ("zstd", &["*.zst", "*.zstd"]),
];

// See `cargo test --lib -- --nocapture default_types::check_duplicates`
#[test]
fn check_duplicates() {
    let mut reverse = std::collections::BTreeMap::new();
    for (name, exts) in DEFAULT_TYPES {
        for ext in *exts {
            reverse.entry(ext).or_insert(Vec::new()).push(name);
        }
    }

    for (ext, names) in reverse {
        if 1 < names.len() {
            println!("{ext} is under multiple names: {names:?}");
        }
    }
}
