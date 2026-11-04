"""Prompts for reactivity letters.

Each builder takes facts only. The tables hold what happened and where
a gift came from; the model writes the letter around them, so two
players who did the same thing still read different letters.
"""

from typing import Dict, List

from chatter_shared import get_language_rule

_FORMAT = (
    'Reply with JSON only: {{"subject": "...", "body": "..."}}.\n'
    'subject: a short letter subject, at most {subject_chars} '
    'characters.\n'
    'body: the whole letter as plain text, at most {body_chars} '
    'characters. Separate paragraphs with a line break. End with a '
    "sign-off in the writer's own name."
)

_IN_WORLD_RULES = (
    "Write as a person living in this world. Never mention levels, "
    "experience, achievements, quests, dungeons as game content, "
    "instances, raids, players, servers or any other game term.\n"
    "Do not invent facts about what the reader did, felt or decided "
    "beyond what is given here. The changes described are only "
    "beginning, never finished."
)


def recipient_line(recipient: Dict) -> str:
    details = ' '.join(
        part for part in (
            recipient.get('gender'),
            recipient.get('race'),
            recipient.get('class'),
        ) if part
    )
    name = recipient.get('name', 'the reader')
    return f"The letter is to {name}, a {details}."


def gift_text(items: List[Dict]) -> str:
    return ', '.join(
        f"{item['name']} x{item['count']}"
        if item.get('count', 1) > 1 else item['name']
        for item in items
    )


def _sender_line(sender: Dict) -> str:
    if sender.get('role'):
        return (
            f"You are {sender['role']}, writing a letter in World of "
            f"Warcraft. It goes out under the name {sender['name']}, "
            "but sign it as who you are."
        )
    return (
        f"You are {sender['name']}, writing a letter in World of "
        "Warcraft."
    )


def _finish(lines: List[str], limits: Dict) -> str:
    lines.append(_FORMAT.format(
        subject_chars=limits['subject_chars'],
        body_chars=limits['body_chars'],
    ))
    prompt = '\n'.join(lines)
    return prompt + get_language_rule()


def deed_letter_prompt(
    sender: Dict, recipient: Dict, row: Dict, items: List[Dict],
    limits: Dict, subject_hint: str = '',
) -> str:
    """Dungeon, raid and quest letters: news first, then the gift."""
    lines = [_sender_line(sender), recipient_line(recipient)]
    if sender.get('location'):
        lines.append(
            f"You are at {sender['location']}. You may name the place "
            'where you sign the letter, with the word "from", or leave '
            "it out, whichever reads better."
        )
    lines += [
        "The reader did this, and you are writing to tell them what "
        "came of it.",
        f"What has changed: {row['letter']}",
        f"The enclosed gift: {gift_text(items)}.",
        f"Where the gift came from: {row['origin']}",
        "If these notes name several possible senders, you are the one "
        "writing this letter.",
        "Write the letter in your own words; do not copy these notes. "
        "First tell what the reader did and how the place has begun to "
        "change, then present the gift, saying how you came by it and "
        "why you send it.",
        _IN_WORLD_RULES,
    ]
    if subject_hint:
        lines.append(f"The subject must be: {subject_hint}")
    return _finish(lines, limits)


def memory_letter_prompt(
    header: str, recipient: Dict, memory: str, items: List[Dict],
    gift_note: str, is_pet: bool, in_world: bool, limits: Dict,
) -> str:
    """A bot writing to someone it shared a moment with."""
    lines = [
        header,
        recipient_line(recipient),
        "You are not travelling with them now and have decided to "
        "write.",
        f"Something you remember together: {memory}",
        f"The enclosed gift: {gift_text(items)}.",
    ]
    if gift_note:
        lines.append(f"About the gift: {gift_note}")
    lines.append(
        "Write in your own voice, in this order: greet them and say "
        "who you are; tell the memory in a few sentences of your own; "
        "whether you hope to meet again depends on your character, so "
        "you may say so or not; then describe the gift, where you got "
        "it and why you want them to have it. Link the gift to the "
        "memory only if a link comes naturally."
    )
    if is_pet:
        lines.append(
            "The gift is a small companion creature. You may say where "
            "you caught it and give it a name."
        )
    lines.append(
        "Do not invent events beyond the memory, and do not write the "
        "reader's words or feelings."
    )
    if in_world:
        lines.append(_IN_WORLD_RULES)
    return _finish(lines, limits)


def starter_letter_prompt(
    trainer: Dict, profession: str, recipient: Dict,
    starter: Dict, limits: Dict,
) -> str:
    """A trainer looking for an apprentice."""
    lines = [
        f"You are {trainer['name']}, a {profession} trainer, writing a "
        "letter in World of Warcraft.",
        recipient_line(recipient),
        "You are looking for an apprentice. You have heard of the "
        "reader and are inviting them to become yours.",
        f"Why {profession} is worth learning, in your own words: "
        f"{starter['why']}",
        f"You enclose these to start with: {gift_text(starter['items'])}."
        " Name them in the letter.",
        f"What they are for: {starter['what']}",
        f"End by saying you can be found at {trainer['place']}, and "
        "inviting them to come to you if they decide to learn.",
        _IN_WORLD_RULES,
    ]
    return _finish(lines, limits)


def profession_letter_prompt(
    trainer: Dict, profession: str, recipient: Dict,
    bundle: Dict, limits: Dict,
) -> str:
    """A trainer sharing surplus materials with a known craftsman."""
    lines = [
        f"You are {trainer['name']}, a {profession} trainer, writing a "
        "letter in World of Warcraft.",
        recipient_line(recipient),
        f"You have heard how the reader's {profession} is coming along "
        "and want to praise it.",
        "You have more supplies than you need and are sending some of "
        f"your surplus: {gift_text(bundle['items'])}.",
        f"What they are good for: {bundle['what']}",
        "Praise them, then say what you are sending and why. Keep it "
        "warm and brief.",
        _IN_WORLD_RULES,
    ]
    return _finish(lines, limits)
