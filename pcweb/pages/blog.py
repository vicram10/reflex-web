import flexdown

import reflex as rx
from pcweb import styles
from pcweb.flexdown import xd
from pcweb.styles import colors as c
from pcweb.styles import text_colors as tc
from pcweb.templates.webpage import webpage

PAGES_PATH = "blog/"


def get_blog_data(paths):
    blogs = {}
    for path in reversed(sorted(paths)):
        document = flexdown.parse_file(path)
        path = path.replace(".md", "")
        blogs[path] = document
    return blogs


def get_route(path: str):
    """Get the route for a page."""
    return path.replace(PAGES_PATH, "").replace(".md", "")


def page(document) -> rx.Component:
    """Create a page."""
    meta = document.metadata
    return rx.chakra.container(
        rx.chakra.heading(meta["title"], padding_bottom="1em", font_weight="semibold"),
        rx.chakra.hstack(
            rx.chakra.avatar(name=meta["author"], size="xs"),
            rx.chakra.text(meta["author"], font_size="0.9rem"),
            rx.chakra.text(" · "),
            rx.chakra.text(str(meta["date"]), font_size="0.9rem"),
            padding_bottom="1em"
        ),
        rx.image(
            src=f"{meta['image']}",
            object_fit="contain",
            shadow="sm",
            my=8,
            border_radius="8px",
        ),
        xd.render(document, "blog.md"),
        padding_bottom="8em",
        margin_top="120px"
    )


paths = flexdown.utils.get_flexdown_files(PAGES_PATH)
blogs = get_blog_data(paths)


class Gallery(rx.Model):
    name: str
    date: str
    tags: list[str]
    description: str
    img: str
    gif: str
    url: str
    source: str


def component_grid():
    posts = []
    for path, document in blogs.items():
        meta = document.metadata
        posts.append(
            rx.link(
                rx.chakra.box(
                    height="10rem",
                    background_image=f'url({meta["image"]})',
                    background_size="cover",
                    background_position="center",
                    background_repeat="no-repeat",
                    border_radius="12px",
                    w="100%",
                ),
                rx.chakra.box(
                    rx.chakra.text(
                        meta["title"],
                        font_size="1.2rem",
                        mb="0.5em",
                        color="#D6D6ED"
                    ),
                    rx.chakra.text(
                        meta["description"],
                        font_size="0.8rem",
                        color="#8E8EA8"

                    ),
                    rx.divider(color="#6C6C81", margin_y="1em"),
                    rx.chakra.hstack(
                        rx.chakra.hstack(
                                rx.chakra.avatar(
                                    name=meta["author"],
                                    size="sm",
                                    bg=c["indigo"][800],
                                    color="#DACEEE",
                                ),
                                rx.chakra.text(meta["author"], font_size="0.8rem"),
                        ),
                        rx.spacer(),
                        rx.chakra.text(str(meta["date"]), font_size="0.8em"),
                        color="#8E8EA8",
                        padding_bottom="0.5em",
                        width="100%",
                    ),
                    height="100%",
                    width="100%",
                    padding_top="1em"
                ),
                overflow="hidden",
                href=path,
            ),
        )
    return rx.chakra.box(
        rx.chakra.responsive_grid(*posts, columns=[1, 2, 2, 2, 3], gap=4),
        padding_top="4em"
    )


@webpage(path="/blog", title="Blog")
def blg():
    return rx.chakra.container(
        rx.vstack(
            rx.vstack(
                rx.flex(
                    rx.chakra.text(
                        "Blog posts", 
                        background_image="linear-gradient(95deg, #B1A9FB 25.71%, #867BF1 83.81%);",
                        text_align="center",
                        background_clip="text",
                        padding_x="1em"
                    ),
                    border_radius= "15px;",
                    border= "1px solid #4435D4;",
                    background= "linear-gradient(180deg, rgba(97, 81, 243, 0.20) 0%, rgba(86, 70, 237, 0.20) 100%);",
                    box_shadow= "0px 3px 6px -3px rgba(34, 25, 121, 0.60), 0px 0px 4px -1px rgba(27, 21, 90, 0.40);"
                ),
                rx.chakra.text(
                    "Reflex Blog Latest News and Updates", 
                    font_size="64px;",
                    background_image="linear-gradient(95deg, #D6D6ED 42.14%, #727280 63.21%);",
                    text_align="center",
                    width="650px",
                    background_clip="text",
                    font_weight="bold",
                    letter_spacing= "-1.28px;",
                ),
                rx.text(
                    "Stay current with all the relevant details for Reflex",
                    color="#6C6C81",
                ),
                align_items="center",
                text_align="left",
                width="100%",
                spacing="1",
            ),
            component_grid(),
            max_width="110em",
            align_items="center",
            min_height="80vh",
            margin_bottom="4em",
            padding_top="95px",
            padding_bottom="2em",
            padding_left = "2em",
            padding_right = "2em",
        ),
        flex_direction="column",
        max_width="960px",
        margin_top="120px"
    )


blog_routes = [blg]
for path, document in blogs.items():
    # Get the docpage component.
    route = f"/{path.replace('.md', '')}"
    title = rx.utils.format.to_snake_case(path.rsplit("/", 1)[1].replace(".md", ""))
    comp = webpage(path=route, title=document.metadata["title"])(
        lambda doc=document: page(doc)
    )

    # Add the route to the list of routes.
    blog_routes.append(comp)
