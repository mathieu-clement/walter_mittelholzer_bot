# Walter Mittelholzer Bot

Hey this is the source code for the Walter Mittelholzer Bot, tooting on
[Mastodon](https://mastodon.citrouille.ch/@walter_mittelholzer_bot).


## Requirements

I'm using a private YOURLS instance (an open source URL shortener) and Mastodon
to publish the images. Therefore you must set the following two environment
variables:

  - `MASTODON_ACCESS_TOKEN`: obtain it from the Development page on the
    web interface of your instance
  - `YOURLS_SIGNATURE`: obtain it from the Tools page in the Admin interface

Do note currently the mastodon instance is hardcoded (see [here](mastodon_client.py)). 
Probably this will be an environment variable in the future.

## Running with podman / docker

Let's build a container named "walter". First check out this repo, then get to work:

```bash
podman build -t walter .
```

Now you should have a working image.

Run it like so:

```bash
podman run --rm \
    -v ./published_images.txt:/src/published_images.txt \
    -e "MASTODON_ACCESS_TOKEN=fJdi2jfi328j-jaslkd" \
    -e "YOURLS_SIGNATURE=29cb29201" \
    walter
```

This will create a new container from the image, fetch an image, 
convert it to JPEG, resize it (Mastodon allows up to 1.6 megapixels only) and create a short
URL and publish a toot to Mastodon.

## Limitations

This program has the following known bugs at the moment:

  - There's no guarantee the resizing and JPEG compression gets us a file under 10 MB as
    required by Mastodon, so it is possible to end up with a file that is too large and
    can't be uploaded.
  - Metadata on Wikimedia Commons is a mess, supposing it's even present on the page, 
    so currently only one type is supported. As a workaround we're using the title of the
    page for the image.
  - If the URL already exists on the YOURLS instance, it won't post. The bug fix here
    is to look at the error from YOURLS and fetch the existing URL.
