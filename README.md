git-foolscap
============

* https://github.com/warner/git-foolscap

git-foolscap is an extension for Git that allows you to publish or access Git repositories over the [Foolscap](http://foolscap.lothar.com/trac) protocol. This provides all the security benefits of ssh or authenticated HTTPS, but with a few important benefits:

* downstream users do not need an account on the server: merely sharing the secret FURL string with them is enough to provide access
* access is limited to the one repository: users do not get full shell access
* servers are quick and easy to set up
* users can easily be limited to read-only access

## Installation

Just use `pip install git-foolscap`. This will install two scripts into your $PATH: `git-foolscap` and `git-remote-pb`. The former is the main entry point, and Git will run it whenever you run `git foolscap COMMAND..`. The latter implements the remote protocol, and Git will use it whenever you access a repository whose remote URL starts with "pb:" (i.e. it is a FURL).

git-foolscap depends upon having Foolscap installed, which depends upon Twisted and pyOpenSSL.

`git-foolscap -h` and `git-foolscap --help` will provide usage instructions. (Note that `git foolscap --help`, without the hyphen, doesn't work, because `git-foolscap` does not provide a man page).

## Theory Of Operation

Repositories are published by running a small server (a Foolscap "flappserver") which listens on a TCP port for encrypted connections. A "FURL" is allocated which will connect to the git remote protocol (in either read+write or read-only mode) for a specific repository. This FURL can be handed to clients, which merely use it as the URL for a standard git remote (e.g. `git clone FURL` or `git remote add NAME FURL`). Foolscap FURLs are URIs which use "`pb:`" as their scheme instead of "`http:`" or "`https:`".

When a git client encounters the `pb:` FURL, it delegates control to a program named `git-remote-pb` (this is a standard feature of git, and holds true for arbitrary scheme names). The `git-remote-pb` program knows how to use Foolscap to connect to the target FURL and speak the git remote protocol through it.

Technically, this means that servers only need the `git-foolscap` executable, and clients only need the `git-remote-pb` executable, but both are distributed in the same package for simplicity.

## Usage: Server

See `git foolscap --help` for full details. Basically the server does this part once:

```
% git foolscap init --port=tcp:3116 --location=tcp:HOSTNAME:3116
% git foolscap start
```

and this part for each new client:

```
% git foolscap invite read-write "comment about recipient"
```

The "invite" will produce a "wormhole code", which the receiving user must type into their "accept" command. The secure FURL will then be sent through the wormhole.

The FURLs can also be added (without invitation) using `git foolscap add`. It must then be cut-and-pasted to the recipient.

To provide read-only access to a single repository, replace `read-write` with `read-only`. You can create as many FURLs as you like, by running `git foolscap add` or `invite` multiple times. Each can be revoked separately. To revoke access, run `git foolscap list`, find the index number, and pass it into `git foolscap revoke`.

You may want to arrange for `git foolscap start` to be run from a cron `@reboot` job, or other boot-time startup script, to make sure that access is retained across a system reboot.

    @reboot cd PATH/TO/REPO && git foolscap start

## Usage: Client

If the repository owner used `git foolscap invite`, then you simply type this code into:

```
% git foolscap accept clone
```

The client can use tab-completion on the codewords, and the wordlist is specifically designed to be reliably transcribeable over a noisy voice channel. 

Instead of cloning a new copy of the repository, you can add the new FURL to an existing repo, by running this command from inside the repository:

```
% git foolscap accept add-remote
```

If the publisher used `git foolscap add` and sent you a full FURL (instead of a wormhole code), then you can just clone from it as you would a normal HTTPS (`https://github.com/warner/git-foolscap.git`) or SSH (`git@github.com:warner/git-foolscap.git`) URL. As long as you have git-foolscap installed, git will figure out how to do the right thing.

## Cleaning up the FURL

The flappserver uses the `--location=` you provide to construct the "connection hints" portion of the FURL. This tells the client how to connect to the server. The server must have a publically-reachable address (or at least reachable by your clients), or you must configure a port-forwarding and put the externally-reachable address+port into the FURL.

If you got the hostname wrong, or if you used an IP address and it has changed, you can edit the FURL later. You can also use multiple hints, and the client will try to connect to each of them until at least one works:

    pb://tvzddtbzbldthde5kdsvjvzpweifx7ae@tcp:example.com:57306,tcp:example.org:57306/jmxpcs6lsmgtuzdomxbgtfcmhgfmfbpc/my-repo

The first big random-looking string in the FURL identifies exactly which server public key is expected: it provides cryptographic assurance that the connection will go to the right server. No certificate authorities or trusted third parties are used. The second random string is a secret "swissnum" which securely identifies the resource being accessed (in this case, a table entry which points at a git repository and a read+write/read-only mode). Knowledge of this secret enables access: to share access, share the secret (and the rest of the FURL necessary to use it); to withhold access, don't reveal the secret.

## Configuring the flappserver

Each flappserver has a "base directory" where it keeps all its state. `git foolscap create` defaults to using `.git/foolscap/` for this purpose, creating it if necessary, then adding an entry for the new FURL.

If you publish multiple repositories, you might want to share flappservers between them, especially if you must configure a port forwarding for each server. To do this, first create the one shared server with Foolscap's `flappserver create BASEDIR` command, then use the `--flappserver=BASEDIR` argument when running `git foolscap init`. This establishes a symlink from `.git/foolscap` to the real BASEDIR, so subsequent git-foolscap commands will add an entry to that flappserver directly. If BASEDIR doesn't already exist, it will be created.

Note that at present, `git foolscap init --flappserver=BASEDIR` requires the `--port=` and `--location=` arguments, even if BASEDIR already exists. However, in that case, their values are ignored in favor of the BASEDIR's existing configuration. Hopefully this will be fixed in a future release.

If you use a `@reboot` cronjob, you may want to use `flappserver start` directly, instead of `git foolscap start`.

## Bugs, Patches

Please file bugs and patches for git-foolscap on the Github issue tracker, at https://github.com/warner/git-foolscap .

For bugs and patches against foolscap itself, please use the Foolscap Trac, at http://foolscap.lothar.com/trac . Foolscap source code is published on Github, at https://github.com/warner/foolscap .

thanks!
