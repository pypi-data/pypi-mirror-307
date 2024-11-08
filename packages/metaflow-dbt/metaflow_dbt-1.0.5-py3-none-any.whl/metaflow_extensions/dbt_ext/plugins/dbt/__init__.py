class dbt_deco:
    def __init__(self, **kwargs):
        self.generate_docs = kwargs.get("generate_docs", False)
        self.kwargs = kwargs

    def __call__(self, step_func):
        # Make generated docs available as a card.
        from metaflow import _dbt, card

        dbt_card = card(type="blank", refresh_interval=1, id="dbt_results")
        if self.generate_docs:

            return dbt_card(card(type="dbt_docs")(_dbt(**self.kwargs)(step_func)))
        else:
            return dbt_card(_dbt(**self.kwargs)(step_func))
