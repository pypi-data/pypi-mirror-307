from metaflow.cards import MetaflowCard, BlankCard
from metaflow.plugins.cards.card_modules.basic import (
    SectionComponent,
    TitleComponent,
    TextComponent,
)


class DBTDocs(MetaflowCard):
    type = "dbt_docs"

    def render(self, task):  # this function returns the HTML to be rendered
        return task.data.static_index


CARDS = [DBTDocs]
