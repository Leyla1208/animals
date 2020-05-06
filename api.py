import flask
from flask import jsonify, request

from data import db_session
from data.models import Feedback

blueprint = flask.Blueprint('api', __name__,
                            template_folder='templates')


@blueprint.route('/api/news')
def get_news():
    session = db_session.create_session()
    news = session.query(Feedback).all()
    return jsonify(
        {
            'feedbacks':
                [item.to_dict(only=('title', 'content', 'user.name'))
                 for item in news]
        }
    )


@blueprint.route('/api/news/<int:id>',  methods=['GET'])
def get_one_news(id):
    session = db_session.create_session()
    feedbacks = session.query(Feedback).get(id)
    if not feedbacks:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'feedbacks': feedbacks.to_dict(only=('title', 'content', 'user_id'))
        }
    )


@blueprint.route('/api/news', methods=['POST'])
def create_news():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['title', 'content', 'user_id']):
        return jsonify({'error': 'Bad request'})
    session = db_session.create_session()
    feedbacks = Feedback(
        title=request.json['title'],
        content=request.json['content'],
        user_id=request.json['user_id']
    )
    session.add(feedbacks)
    session.commit()
    return jsonify({'success': 'OK'})