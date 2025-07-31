import pytest

from home.forms import ArticleForm


@pytest.mark.django_db
def test_form_with_valid_data():
    form_data = {
        "title": "test_title",
        "markdown_content": "test_content",
    }
    form = ArticleForm(data=form_data)

    assert form.is_valid()


@pytest.mark.django_db
@pytest.mark.parametrize(
    "error_field, form_data",
    [
        ("title", {"title": None, "markdown_content": "test_content"}),
        ("markdown_content", {"title": "test_title", "markdown_content": None}),
    ],
    ids=["missing_title", "missing_content"],
)
def test_form_without_required_fields(error_field, form_data):
    form = ArticleForm(data=form_data)

    assert not form.is_valid()
    assert error_field in form.errors
