import app.http.request as request
import app.tags.tag_controller as tags
from app.tags.tag_schema import GetAllTagsResponse


def register_routes(app):
    @app.route("/getAllTags", methods=["POST"])
    def _get_all_tags():
        return request.invoke(tags.get_all_tags, None, GetAllTagsResponse(many=True))
