from drf_yasg import openapi




def OrderDataSchema():
    schema = openapi.Schema(
        type = openapi.TYPE_OBJECT,
        properties={
          'name': openapi.Schema(type = openapi.TYPE_STRING, description="string"),
          'status': openapi.Schema(type = openapi.TYPE_STRING, description="string"),
          'type': openapi.Schema(type = openapi.TYPE_STRING, description="string"),
          'pk': openapi.Schema(type = openapi.TYPE_STRING, description="integer"),
          'img': openapi.Schema(type = openapi.TYPE_STRING, description="string"),
          'image': openapi.Schema(type = openapi.TYPE_STRING, description="string"),
                  }
    )
    return schema
def OrderListSchema():
     schema = openapi.Schema(
     type=openapi.TYPE_OBJECT,
     properties={'data':openapi.Schema(type=openapi.TYPE_ARRAY, description="array", items = OrderDataSchema()),
               'request_id':openapi.Schema(type = openapi.TYPE_STRING, description="request id integer")}
     )
     return schema
