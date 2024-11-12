from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse
from square_commons import get_api_output_in_standard_format
from square_database_helper.main import SquareDatabaseHelper
from square_database_structure.square import global_string_database_name
from square_database_structure.square.greeting import global_string_schema_name
from square_database_structure.square.greeting.tables import Greeting

from square_common_bl.configuration import (
    global_object_square_logger,
    config_str_square_database_ip,
    config_int_square_database_port,
    config_str_square_database_protocol,
)
from square_common_bl.messages import messages
from square_common_bl.pydantic_models.greeting import CreateGreetingV0

router = APIRouter(
    tags=["greeting"],
)

global_object_square_database_helper = SquareDatabaseHelper(
    param_str_square_database_ip=config_str_square_database_ip,
    param_int_square_database_port=config_int_square_database_port,
    param_str_square_database_protocol=config_str_square_database_protocol,
)


@router.post("/create_greeting/v0")
@global_object_square_logger.async_auto_logger
async def create_greeting_v0(body: CreateGreetingV0):
    app_id = body.app_id
    greeting_is_anonymous = body.greeting_is_anonymous
    greeting_anonymous_sender_name = body.greeting_anonymous_sender_name
    if body.user_id:
        user_id = str(body.user_id)
    else:
        user_id = body.user_id
    greeting_text = body.greeting_text
    try:

        """
        validation
        """
        # validate user id
        if not greeting_is_anonymous and user_id is None:
            output_content = get_api_output_in_standard_format(
                message=messages["GENERIC_400"],
                log="provide user id for non-anonymous greetings.",
            )
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=output_content,
            )

        """
        main process
        """
        # add greeting to the table
        local_list = global_object_square_database_helper.insert_rows_v0(
            database_name=global_string_database_name,
            schema_name=global_string_schema_name,
            table_name=Greeting.__tablename__,
            data=[
                {
                    Greeting.app_id.name: app_id,
                    Greeting.greeting_is_anonymous.name: greeting_is_anonymous,
                    Greeting.greeting_anonymous_sender_name.name: greeting_anonymous_sender_name,
                    Greeting.user_id.name: user_id,
                    Greeting.greeting_text.name: greeting_text,
                },
            ],
        )

        """
        return value
        """

        output_content = get_api_output_in_standard_format(
            message=messages["GENERIC_CREATION_SUCCESSFUL"],
            data={"main": local_list["data"]["main"]},
        )
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=output_content,
        )
    except HTTPException as http_exception:
        return JSONResponse(
            status_code=http_exception.status_code, content=http_exception.detail
        )
    except Exception as e:
        """
        rollback logic
        """
        global_object_square_logger.logger.error(e, exc_info=True)
        output_content = get_api_output_in_standard_format(
            message=messages["GENERIC_500"],
            log=str(e),
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=output_content,
        )
