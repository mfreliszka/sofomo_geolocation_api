"""Module containing Sqlalchemy models."""

from sqlalchemy import Column, Numeric, String
# from sqlalchemy.orm import relationship

from app.db.models.base import Base, BaseDBModel
from app.db.models.metadata import metadata_family


class IPGeolocation(Base, BaseDBModel):
    """Database model representing 'parent' table in db."""

    __metadata__ = metadata_family

    ip = Column(String, index=True, unique=True)
    type = Column(String)
    continent_code = Column(String)
    continent_name = Column(String)
    country_code = Column(String)
    country_name = Column(String)
    region_code = Column(String)
    region_name = Column(String)
    city = Column(String)
    zip = Column(String)
    latitude = Column(Numeric(precision=16, scale=13))
    longitude = Column(Numeric(precision=16, scale=13))

    # children = relationship("Child", back_populates="parent")


# {
#     "ip": "8.8.8.8",
#     "type": "ipv4",
#     "continent_code": "NA",
#     "continent_name": "North America",
#     "country_code": "US",
#     "country_name": "United States",
#     "region_code": "OH",
#     "region_name": "Ohio",
#     "city": "Glenmont",
#     "zip": "44628",
#     "latitude":  40.5369987487793,
#     "longitude": -82.12859344482422,
#     "msa": null,
#     "dma": "510",
#     "radius": null,
#     "ip_routing_type": "fixed",
#     "connection_type": "ocx",
#     "location": {
#         "geoname_id": null,
#         "capital": "Washington D.C.",
#         "languages": [
#             {
#                 "code": "en",
#                 "name": "English",
#                 "native": "English"
#             }
#         ],
#         "country_flag": "https://assets.ipstack.com/flags/us.svg",
#         "country_flag_emoji": "🇺🇸",
#         "country_flag_emoji_unicode": "U+1F1FA U+1F1F8",
#         "calling_code": "1",
#         "is_eu": false
#     }
# }
