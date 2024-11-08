import winzy
import requests
import os
import hashlib
from datetime import datetime


def get_random_filename(ext=".jpg"):
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S")
    filename = hashlib.sha256(timestamp.encode()).hexdigest()[:20] + ext
    return filename


def create_parser(subparser):
    parser = subparser.add_parser(
        "txt2img", description="Generate text to image using pollinations.ai api"
    )
    parser.add_argument(
        "-p",
        "--prompt",
        type=str,
        nargs="*",
        required=True,
        help="Prompt for the image URL",
    )
    parser.add_argument(
        "-o", "--output", type=str, default=None, help="Output filename (default: None)"
    )
    parser.add_argument(
        "-w", "--width", type=int, default=None, help="Image Width default None"
    )
    parser.add_argument(
        "-hi", "--height", type=int, default=None, help="Image height default None"
    )
    parser.add_argument(
        "-s", "--seed", type=int, default=None, help="Seed to use default None"
    )
    parser.add_argument(
        "-m",
        "--model",
        type=str,
        default=None,
        help="Model to use ex: 'flux' default None",
    )
    parser.add_argument(
        "-sh", "--show", action="store_true", help="If given show the downloaded file"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="If given show the downloaded file"
    )

    return parser


def download_image(
    prompt,
    filename=None,
    width=None,
    height=None,
    seed=None,
    model=None,
    show=False,
    verbose=False,
):

    if prompt:
        prompt_str = " ".join(prompt)

    url = f"https://pollinations.ai/p/{prompt_str}"
    if width:
        url += f"?width={width}"
    if height:
        url += f"?height={height}"
    if seed:
        url += f"&seed={seed}"
    if model:
        url += f"&model={model}"

    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error: Response Code: {response.status_code}")
        print(f"{response.text}")

    if verbose:
        print(response)

    if filename is None:
        filename = get_random_filename()
    # if path is provided but no file extention then
    elif "." not in filename and os.path.exists(filename):
        filename = os.path.join(filename, get_random_filename())

    with open(filename, "wb") as file:
        file.write(response.content)
    print(f"{filename}")

    if show:
        os.startfile(filename)


class HelloWorld:
    """ An example plugin """

    __name__ = "txt2img"

    @winzy.hookimpl
    def register_commands(self, subparser):
        parser = create_parser(subparser)
        parser.set_defaults(func=self.generate)

    def generate(self, args):
        _ = download_image(
            args.prompt,
            filename=args.output,
            width=args.width,
            height=args.height,
            seed=args.seed,
            model=args.model,
            show=args.show,
            verbose=args.verbose,
        )

    def hello(self, args):
        # this routine will be called when "winzy "txt2img is called."
        print("Hello! This is an example ``winzy`` plugin.")


txt2img_plugin = HelloWorld()
