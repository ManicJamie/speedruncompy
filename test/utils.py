from typing import TypeVar

from speedruncompy.datatypes import SpeedrunModel

SrcompyModel = TypeVar("SrcompyModel", bound=SpeedrunModel)

def check_model_coverage(m: SpeedrunModel):
    """Assert that a model has all its members"""
    if m.model_extra is None:
        raise Exception("Tests must be run with config.extra == 'allow'!")  # noqa: TRY002
    assert len(m.model_extra) == 0, f"Model {type(m)} is missing provided keys: {[f'{k} = {v}' for k, v in m.model_extra.items()]}"

def check_pages(pages: dict[int, SrcompyModel]):
    for model in pages.values():
        check_model_coverage(model)
