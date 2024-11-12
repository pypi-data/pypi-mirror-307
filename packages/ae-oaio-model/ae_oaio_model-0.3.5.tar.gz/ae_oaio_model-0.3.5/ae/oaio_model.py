""" Our Asynchronously Interchangeable Objects Data Structures

"""
import dataclasses
import datetime

from dataclasses import dataclass, field
from typing import Any, MutableMapping, Optional, Sequence

from ae.base import NOW_STR_FORMAT, now_str, defuse                                             # type: ignore


__version__ = '0.3.5'


CREATE_WRITE_ACCESS = 'c'           #: create, delete and update rights, see write_access field in Pubz and Userz
DELETE_WRITE_ACCESS = 'd'           #: delete and update rights
UPDATE_WRITE_ACCESS = 'u'           #: only update rights
READ_ONLY_ACCESS = ''
ACCESS_RIGHTS = (CREATE_WRITE_ACCESS, DELETE_WRITE_ACCESS, UPDATE_WRITE_ACCESS, READ_ONLY_ACCESS)   #: all access rights

DELETE_ACTION = 'delete'            #: object got deleted, not used in Logz.action field (records get deleted instead)
DOWNLOAD_ACTION = 'download'        #: object got downloaded/synced
UPLOAD_ACTION = 'upload'            #: object got uploaded/updated
REGISTER_ACTION = 'register'        #: oaio got registered
LOG_DB_ACTIONS = (REGISTER_ACTION, UPLOAD_ACTION, DOWNLOAD_ACTION)  #: see Logz.action field
LOG_ACTIONS = LOG_DB_ACTIONS + (DELETE_ACTION, )
UPDATE_ACTIONS = (REGISTER_ACTION, UPLOAD_ACTION)

NAME_VALUES_KEY = '_name'           #: oaio values key of optional object name
ROOT_VALUES_KEY = '_root_path'      #: oaio values key of optional files root path
FILES_VALUES_KEY = '_file_paths'    #: oaio values key of paths list of optional files attached to an oaio

OBJECTS_DIR = 'objz'                #: name of folder to store infos of oai objects not yet synced with server
FILES_DIR = 'filez'                 #: name of folder to store file names attached to an oaio

HTTP_HEADER_USR_ID = 'X-OAIO-user'  #: user name
HTTP_HEADER_APP_ID = 'X-OAIO-app'   #: app id
HTTP_HEADER_DVC_ID = 'X-OAIO-dvc'   #: device id

MAX_STAMP_DIFF = 69.0               #: maximum accepted UTC time difference in seconds between client and server
OLDEST_SYNC_STAMP = '20221231111111012345'      #: oldest complete stamp ("" is even older)
STAMP_FORMAT = NOW_STR_FORMAT.format(sep="")    #: stamp format string


now_stamp = now_str                 #: function alias used to create a new oaio stamp


ActionType = str                    #: register/upload/download... action type
OaioDictType = dict[str, Any]       #: type of oai object converted into a dictionary

OaioIdType = str                    #: oai object id
OaioAppIdType = str                 #: app id
OaioCshIdType = str                 #: cloud storage host id
OaioCshWriteAccessType = str        #: write access rights (:attr:`oaio_server.oapi.models.Pubz.write_access`)
OaioDeviceIdType = str              #: device id
OaioRootPathType = str              #: default root path (containing :data:`~ae.paths.PATH_PLACEHOLDERS`)
OaioStampType = str                 #: oaio stamp
OaioUserIdType = str                #: Userz.Uid/auth.User.username
OaioValuesType = dict[str, Any]     #: oaio client_values and server_values

OaioFilesType = Sequence[str]       #: item type of the :data:`FILES_VALUES_KEY` within :attr:`OaiObject.client_values`


@dataclass
class OaiObject:
    """ oaio data types and structures """
    oaio_id: OaioIdType

    client_stamp: OaioStampType = ''                                #: timestamp of register or newest upload
    server_stamp: OaioStampType = ''                                #: timestamp of previous version

    client_values: OaioValuesType = field(default_factory=dict)     #: actual object values
    server_values: OaioValuesType = field(default_factory=dict)     #: previous object values (for debugging/monitoring)

    csh_id: Optional[OaioCshIdType] = None                          #: cloud storage host id (for attached file/folders)
    csh_write_access: OaioCshWriteAccessType = ''                   #: write access rights

    # optional fields used in synchronization to store updated server values from other user/device/app
    username: OaioUserIdType = ''                                   #: name of the actual user
    device_id: OaioDeviceIdType = ''                                #: id of the actual device
    app_id: OaioAppIdType = ''                                      #: id of the actual application


OaioMapType = MutableMapping[OaioIdType, OaiObject]


# *************************  helpers  ************************************************************


def extra_headers(user_name: OaioUserIdType, device_id: OaioDeviceIdType, app_id: OaioAppIdType = '') -> dict[str, str]:
    """ add extra headers into the returned dictionary (used e.g. in Client(headers=...)

    :param user_name:
    :param device_id:
    :param app_id:
    :return:
    """
    return {
        HTTP_HEADER_USR_ID: user_name,
        HTTP_HEADER_DVC_ID: device_id,
        HTTP_HEADER_APP_ID: app_id,
        }


def object_dict(oai_obj: OaiObject) -> OaioDictType:
    """ convert OaiObject dataclass instance into the corresponding mapping/dict object.

    :param oai_obj:             oai object to convert.
    :return:                    converted dict object.
    """
    # Pycharm bug https://youtrack.jetbrains.com/issue/PY-76070
    # noinspection PyTypeChecker
    return dataclasses.asdict(oai_obj)


def object_id(user_name: OaioUserIdType, device_id: OaioDeviceIdType, app_id: OaioAppIdType,
              stamp: OaioStampType, values: OaioValuesType) -> OaioIdType:
    """ generate object id (of type OaioIdType) from the specified arguments.

    :param user_name:           username of the object creator/registrar.
    :param device_id:           id of the device from where the object get registered.
    :param app_id:              id of the registering application.
    :param stamp:               timestamp when the object got registered.
    :param values:              values of the object.
    :return:                    oai object id (can be used as file name on most OS).
    :raises:                    AssertationError if one of the following arguments is empty:
                                :paramref:`object_id.user_name`, :paramref:`object_id.device_id`,
                                :paramref:`object_id.app_id` or :paramref:`object_id.stamp`.
    """
    assert user_name and device_id and app_id and stamp, f"empty usr={user_name} dvc={device_id} app={app_id} s={stamp}"
    obj_url = f'{app_id}://{user_name}@{device_id}'

    if NAME_VALUES_KEY in values:
        obj_url += '/' + values[NAME_VALUES_KEY]
    elif ROOT_VALUES_KEY in values:
        obj_url += '/' + values[ROOT_VALUES_KEY].strip('/')     # remove leading/trailing path separator character
    elif len(values.get(FILES_VALUES_KEY, [])) == 1:
        obj_url += '/' + values[FILES_VALUES_KEY][0]

    obj_url += '/' + stamp

    return defuse(obj_url)


def stamp_diff(stamp1: OaioStampType, stamp2: OaioStampType) -> float:
    """ determine the difference in seconds between the two specified stamps in the format %Y%m%d%H%M%S%f.

    :param stamp1:              time stamp string 1 (return positive seconds value if older than stamp2).
    :param stamp2:              time stamp string 2.
    :return:                    float with the difference in seconds between both specified stamps (stamp2 - stamp1).
    """
    parser = datetime.datetime.strptime
    return (parser(stamp2, STAMP_FORMAT) - parser(stamp1, STAMP_FORMAT)).total_seconds()
