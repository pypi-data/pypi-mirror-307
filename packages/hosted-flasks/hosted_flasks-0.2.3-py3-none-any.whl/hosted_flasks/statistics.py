import logging


from dataclasses import dataclass, field, fields
from typing import Union, Dict, List

from datetime import datetime
import humanize
from ua_parser import user_agent_parser

from flask.globals import request_ctx

import json
import os
import pymongo

logger = logging.getLogger(__name__)

DB_CONN = os.environ.get("MONGODB_URI", "mongodb://localhost:27017/hosted")
DB_NAME = DB_CONN.split("/")[-1].split("?")[0]

db = None

try:
  client = pymongo.MongoClient(DB_CONN)
  logger.debug(json.dumps(client.server_info(), indent=2, default=str))
  db = client[DB_NAME]
except Exception as err:
  logger.exception(err)

@dataclass
class LogConfig:
  args       : bool = True
  url        : bool = True
  user_agent : bool = True
  remote_addr: bool = True
  referrer   : bool = True
  endpoint   : bool = True
  path       : bool = True
  headers    : List[str] = field(default_factory=list)

  def analyze(self, request):
    analysis = {
      "datetime"    : datetime.now(),
      "args"        : dict(request.args),
      "url"         : request.url,
      "user_agent"  : user_agent_parser.Parse(request.user_agent.string),
      "remote_addr" : request.remote_addr,
      "referrer"    : request.referrer,
      "endpoint"    : request.endpoint,
      "path"        : request.path
    }
    for fld in fields(self):
      if not getattr(self, fld.name):
        analysis.pop(fld.name, None)

    for header in self.headers:
      analysis[header] = request.headers.get(header, None)
    
    return analysis

class Tracker:
  def __init__(self, hostedflask):
    self.hostedflask = hostedflask
    self.started     = datetime.now()
    self.hits        = 0

    try:
      self.hostedflask.handler.extensions["hosted-flasks-tracker"]
      logger.warning("f📊 {self.hostedflask.name} already has tracker")
    except KeyError:
      logger.info(f"📊 setting up tracker for {self.hostedflask.name}")
      self.hostedflask.handler.extensions["hosted-flasks-tracker"] = self
      self.hostedflask.handler.before_request(self.before_request)

  @property
  def humanized_since(self):
    return humanize.naturaltime(self.started)

  def before_request(self):
    self.track_request(request_ctx.request)

  def track_request(self, request):
    if request.endpoint in self.hostedflask.track:
      analytics = self.hostedflask.log.analyze(request)
      logger.info(f"📊 [{self.hostedflask.name}] {analytics}")
      self.hits += 1
      if db is not None:
        analytics["metadata"] = { "hosted_flask": self.hostedflask.name }
        db.logs.insert_one(analytics)

def track(hostedflask):
  Tracker(hostedflask)
  return hostedflask

"""
db.createCollection(
   "logs",
   {
      timeseries: {
         timeField: "datetime",
         metaField: "metadata",
         granularity: "seconds"
      },
      expireAfterSeconds: 2592000
   }
)
  
db.logs.aggregate( [
   {
      $project: {
         date: {
            $dateToParts: { date: "$datetime" }
         },
         site: "$metadata.hosted_flask" 
      }
   },
   {
      $group: {
         _id: {
            site: "$site",
            date: {
               year: "$date.year",
               month: "$date.month",
               day: "$date.day",
               hour: "$date.hour"
            }
         },
         visitors: { $sum: 1 }
      }
   }
] )
"""
