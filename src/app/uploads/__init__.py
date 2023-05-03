import app.http.request as request
import app.uploads.upload_controller as upload
from app.uploads.upload_schema import GetUploadsRequestSchema, GetUploadsResponseSchema


def register_routes(app):
    @app.route("/getUploads", methods=["POST"])
    def _get_uploads():
        return request.invoke(
            upload.get_uploads,
            GetUploadsRequestSchema(),
            GetUploadsResponseSchema(many=True),
        )

    @app.route("/addUpload", methods=["POST"])
    def _get_upload():
        return request.invoke(
            upload.add_upload,
            None,
            GetUploadsResponseSchema(many=True),
        )
