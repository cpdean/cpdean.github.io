import enum
import attr


class Color(enum.Enum):
    red = 1
    green = 2
    purple = 3


class Shape(enum.Enum):
    bean = 1
    pill = 2
    diamond = 3


class Count(enum.Enum):
    one = 1
    two = 2
    three = 3


class Texture(enum.Enum):
    clear = 1
    stripe = 2
    solid = 3


@attr.s
class Card(object):
    color = attr.ib()
    shape = attr.ib()
    count = attr.ib()
    texture = attr.ib()


def all_cards():
    for color in Color:
        for shape in Shape:
            for count in Count:
                for texture in Texture:
                    yield Card(
                        color=color,
                        shape=shape,
                        count=count,
                        texture=texture,
                    )


def is_set(cards):
    if len(cards) != 3:
        return False

    def same_or_diff(items):
        return (
            len(set(items)) == 3
            or
            len(set(items)) == 1
        )

    colors = same_or_diff([i.color for i in cards])
    shapes = same_or_diff([i.shape for i in cards])
    counts = same_or_diff([i.count for i in cards])
    textures = same_or_diff([i.texture for i in cards])
    return colors and shapes and counts and textures


def test_is_set():
    c = lambda n: Card(
        color=Color.red,
        shape=Shape.diamond,
        count=n,
        texture=Texture.clear,
    )

    assert is_set(
        [
            c(Count.one),
            c(Count.two),
            c(Count.three),
        ]
    )


def test_is_not_set():
    c = lambda n: Card(
        color=Color.red,
        shape=Shape.diamond,
        count=n,
        texture=Texture.clear,
    )

    assert not is_set(
        [
            c(Count.one),
            c(Count.two),
            Card(
                color=Color.green,
                shape=Shape.diamond,
                count=Count.three,
                texture=Texture.clear
            )
        ]
    )


def test_deck_size():
    assert len(list(all_cards())) == 81


def test_look_for_matches_in_a_board():
    assert False
