from flask import Blueprint, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired

import people_web_app.adapters.repository as repo

people_blueprint = Blueprint(
    'people_bp', __name__
)


@people_blueprint.route('/')
def home():
    return render_template(
        'home.html',
        find_person_url=url_for('people_bp.find_person'),
        list_people_url=url_for('people_bp.list_people')
    )


@people_blueprint.route('/list')
def list_people():
    return render_template(
        'list_people.html',
        people=repo.repo_instance,
        find_person_url=url_for('people_bp.find_person'),
        list_people_url=url_for('people_bp.list_people'))


@people_blueprint.route('/find', methods=['GET', 'POST'])
def find_person():
    form = SearchForm()

    # If the method is POST and validation has passed
    if form.validate_on_submit():
        return render_template(
            'list_person.html',
            person=repo.repo_instance.get_person(form.person_id.data),
            find_person_url=url_for('people_bp.find_person'),
            list_people_url=url_for('people_bp.list_people')
        )

    # If the method is POST and validation didn't pass OR the method is GET
    return render_template(
        'find_person.html',
        find_person_url=url_for('people_bp.find_person'),
        list_people_url=url_for('people_bp.list_people'),
        form=form,
        handler_url=url_for('people_bp.find_person')
    )


class SearchForm(FlaskForm):
    person_id = IntegerField('Person id', [
        DataRequired(message='A person id is required')
    ])
    submit = SubmitField('Find')
