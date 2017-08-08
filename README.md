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

To provide read-only access to a single repository, run `git foolscap create --port=ENDPOINT --location=HINT read-only COMMENT` from within the repo's directory. "COMMENT" should be a single string (with quotes if it includes spaces) that reminds you about who you're providing access to: it will be recorded and made available to `git foolscap list` later, in case you want to selectively revoke acess in the future. `create` will print the FURL that should be delivered to your clients.

`ENDPOINT` tells the server what TCP port to listen on, and should look something like `tcp:12345`. `HINT` tells it what network location to advertise, for which you'll need to know an externally-reachable hostname or IP address. The hint should look something like `tcp:example.org:12345`. Both must be supplied.

Then run `git foolscap start` to launch the server.

You can create as many FURLs as you like, by running `git foolscap create` multiple times. Each can be revoked separately. Use `git foolscap list` to see them all, and `git foolscap revoke` to revoke one.

You may want to arrange for `git foolscap start` to be run from a cron `@reboot` job, or other boot-time startup script, to make sure that access is retained across a system reboot.

    @reboot cd PATH/TO/REPO && git foolscap start

## Usage: Client

Once someone gives you a FURL, you can simply clone from it as you would a normal HTTPS (`https://github.com/warner/git-foolscap.git`) or SSH (`git@github.com:warner/git-foolscap.git`) URL. As long as you have git-foolscap installed, git will figure out how to do the right thing.

## Cleaning up the FURL

The flappserver uses the `--location=` you provide to construct the "connection hints" portion of the FURL. This tells the client how to connect to the server. The server must have a publically-reachable address (or at least reachable by your clients), or you must configure a port-forwarding and put the externally-reachable address+port into the FURL.

If you got the hostname wrong, or if you used an IP address and it has changed, you can edit the FURL later. You can also use multiple hints, and the client will try to connect to each of them until at least one works:

    pb://tvzddtbzbldthde5kdsvjvzpweifx7ae@example.com:57306,example.org:57306/jmxpcs6lsmgtuzdomxbgtfcmhgfmfbpc/my-repo

The first big random-looking string in the FURL identifies exactly which server public key is expected: it provides cryptographic assurance that the connection will go to the right server. No certificate authorities or trusted third parties are used. The second random string is a secret "swissnum" which securely identifies the resource being accessed (in this case, a table entry which points at a git repository and a read+write/read-only mode). Knowledge of this secret enables access: to share access, share the secret (and the rest of the FURL necessary to use it); to withhold access, don't reveal the secret.

## Configuring the flappserver

Each flappserver has a "base directory" where it keeps all its state. `git foolscap create` defaults to using `.git/foolscap/` for this purpose, creating it if necessary, then adding an entry for the new FURL.

If you publish multiple repositories, you might want to share flappservers between them, especially if you must configure a port forwarding for each server. To do this, first create the one shared server with Foolscap's `flappserver create BASEDIR` command, then for each new access FURL, use `git-foolscap`'s `--flappserver=BASEDIR` option:

    git foolscap --flappserver=BASEDIR create --port=ENDPOINT --location=LOCATION read-write COMMENT

This will cause git-foolscap to add an entry to the flappserver in BASEDIR instead of creating and/or modifying the one in `.git/foolscap`. If you use a `@reboot` cronjob, you may want to use `flappserver start` directly, instead of `git foolscap start`.

If you create the flappserver with `flappserver create`, you can provide options to set the published location, or the port on which it will listen. See `flappserver create --help` for details. You can also edit the config files inside the flappserver directory after creation (`port` controls what TCP port the server listens on, and `furl_prefix` is used when generating new FURLs).

## Bugs, Patches

Please file bugs and patches for git-foolscap on the Github issue tracker, at https://github.com/warner/git-foolscap .

For bugs and patches against foolscap itself, please use the Foolscap Trac, at http://foolscap.lothar.com/trac . Foolscap source code is published on Github, at https://github.com/warner/foolscap .

thanks!
