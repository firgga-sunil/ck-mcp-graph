Request
./

Response

{
  "version": "demo--595",
  "domainName": "demo",
  "lookupData": {
    "subsytems": {
      "ss:Tix-Tyrion": {
        "id": "ss:Tix-Tyrion",
        "name": "Tix-Tyrion",
        "kind": "subsystem::cluster",
        "details": [
          {
            "key": "RESOURCEKINDS",
            "type": "list",
            "value": [
              "KAFKA_CONSUMER",
              "MONGODB"
            ]
          },
          {
            "key": "NESTEDDEPLOYMENT",
            "type": "integer",
            "value": 2
          }
        ],
        "uiDetails": {
          "visibility": "collapsed",
          "display": "active"
        }
      },
      "ss:Tix-Raven": {
        "id": "ss:Tix-Raven",
        "name": "Tix-Raven",
        "kind": "subsystem::cluster",
        "details": [
          {
            "key": "NESTEDDEPLOYMENT",
            "type": "integer",
            "value": 1
          },
          {
            "key": "RESOURCEKINDS",
            "type": "list",
            "value": [
              "KAFKA_CONSUMER"
            ]
          }
        ],
        "uiDetails": {
          "visibility": "collapsed",
          "display": "active"
        }
      },
      "ss:External::INBOUND": {
        "id": "ss:External::INBOUND",
        "name": "External::INBOUND",
        "kind": "subsystem::simple",
        "details": [
          {
            "key": "RESOURCEKINDS",
            "type": "list",
            "value": [
              "EXTERNAL"
            ]
          },
          {
            "key": "NESTEDDEPLOYMENT",
            "type": "integer",
            "value": 1
          }
        ],
        "uiDetails": {
          "visibility": "collapsed",
          "display": "active"
        }
      },
      "ss:Tix-Winterfell": {
        "id": "ss:Tix-Winterfell",
        "name": "Tix-Winterfell",
        "kind": "subsystem::cluster",
        "details": [
          {
            "key": "NESTEDDEPLOYMENT",
            "type": "integer",
            "value": 2
          },
          {
            "key": "RESOURCEKINDS",
            "type": "list",
            "value": [
              "JAVA",
              "MONGODB"
            ]
          }
        ],
        "uiDetails": {
          "visibility": "collapsed",
          "display": "active"
        }
      },
      "ss:KAFKA::review_moderation": {
        "id": "ss:KAFKA::review_moderation",
        "name": "KAFKA::review_moderation",
        "kind": "subsystem::cluster",
        "details": [
          {
            "key": "NESTEDDEPLOYMENT",
            "type": "integer",
            "value": 1
          },
          {
            "key": "RESOURCEKINDS",
            "type": "list",
            "value": [
              "KAFKA"
            ]
          }
        ],
        "uiDetails": {
          "visibility": "collapsed",
          "display": "active"
        }
      },
      "ss:Tix-Eyrie-V2": {
        "id": "ss:Tix-Eyrie-V2",
        "name": "Tix-Eyrie-V2",
        "kind": "subsystem::cluster",
        "details": [
          {
            "key": "NESTEDDEPLOYMENT",
            "type": "integer",
            "value": 2
          },
          {
            "key": "RESOURCEKINDS",
            "type": "list",
            "value": [
              "GO",
              "SQL"
            ]
          }
        ],
        "uiDetails": {
          "visibility": "collapsed",
          "display": "active"
        }
      }
    },
    "systemUnits": {
      "su:Tix-Eyrie-V2::App": {
        "id": "su:Tix-Eyrie-V2::App",
        "name": "Tix-Eyrie-V2::App",
        "kind": "systemunit::app",
        "parentId": "ss:Tix-Eyrie-V2",
        "details": [
          {
            "key": "RUNTIME",
            "type": "string",
            "value": "GO"
          },
          {
            "key": "STORAGE_TYPES",
            "type": "list",
            "value": [
              "SQL"
            ]
          }
        ],
        "uiDetails": {
          "visibility": "expanded",
          "display": "active"
        }
      },
      "su:Tix-Raven::App": {
        "id": "su:Tix-Raven::App",
        "name": "Tix-Raven::App",
        "kind": "systemunit::app",
        "parentId": "ss:Tix-Raven",
        "details": [
          {
            "key": "RUNTIME",
            "type": "string",
            "value": "KAFKA_CONSUMER"
          }
        ],
        "uiDetails": {
          "visibility": "expanded",
          "display": "active"
        }
      },
      "su:KAFKA::review_moderation": {
        "id": "su:KAFKA::review_moderation",
        "name": "KAFKA::review_moderation",
        "kind": "systemunit::queue",
        "parentId": "ss:KAFKA::review_moderation",
        "details": [
          {
            "key": "RUNTIME",
            "type": "string",
            "value": "KAFKA"
          }
        ],
        "uiDetails": {
          "visibility": "expanded",
          "display": "active"
        }
      },
      "su:Tix-Tyrion::Mongo": {
        "id": "su:Tix-Tyrion::Mongo",
        "name": "Tix-Tyrion::Mongo",
        "kind": "systemunit::storage",
        "parentId": "ss:Tix-Tyrion",
        "details": [
          {
            "key": "RUNTIME",
            "type": "string",
            "value": "MONGODB"
          }
        ],
        "uiDetails": {
          "visibility": "collapsed",
          "display": "active"
        }
      },
      "su:External::INBOUND": {
        "id": "su:External::INBOUND",
        "name": "External::INBOUND",
        "kind": "systemunit::external",
        "parentId": "ss:External::INBOUND",
        "details": [
          {
            "key": "RUNTIME",
            "type": "string",
            "value": "EXTERNAL"
          }
        ],
        "uiDetails": {
          "visibility": "expanded",
          "display": "active"
        }
      },
      "su:Tix-Winterfell::App": {
        "id": "su:Tix-Winterfell::App",
        "name": "Tix-Winterfell::App",
        "kind": "systemunit::app",
        "parentId": "ss:Tix-Winterfell",
        "details": [
          {
            "key": "STORAGE_TYPES",
            "type": "list",
            "value": [
              "MONGODB"
            ]
          },
          {
            "key": "RUNTIME",
            "type": "string",
            "value": "JAVA"
          }
        ],
        "uiDetails": {
          "visibility": "expanded",
          "display": "active"
        }
      },
      "su:Tix-Winterfell::Mongo": {
        "id": "su:Tix-Winterfell::Mongo",
        "name": "Tix-Winterfell::Mongo",
        "kind": "systemunit::storage",
        "parentId": "ss:Tix-Winterfell",
        "details": [
          {
            "key": "RUNTIME",
            "type": "string",
            "value": "MONGODB"
          }
        ],
        "uiDetails": {
          "visibility": "collapsed",
          "display": "active"
        }
      },
      "su:Tix-Eyrie-V2::mysql": {
        "id": "su:Tix-Eyrie-V2::mysql",
        "name": "Tix-Eyrie-V2::mysql",
        "kind": "systemunit::storage",
        "parentId": "ss:Tix-Eyrie-V2",
        "details": [
          {
            "key": "RUNTIME",
            "type": "string",
            "value": "SQL"
          }
        ],
        "uiDetails": {
          "visibility": "collapsed",
          "display": "active"
        }
      },
      "su:Tix-Tyrion::App": {
        "id": "su:Tix-Tyrion::App",
        "name": "Tix-Tyrion::App",
        "kind": "systemunit::app",
        "parentId": "ss:Tix-Tyrion",
        "details": [
          {
            "key": "STORAGE_TYPES",
            "type": "list",
            "value": [
              "MONGODB"
            ]
          },
          {
            "key": "RUNTIME",
            "type": "string",
            "value": "KAFKA_CONSUMER"
          }
        ],
        "uiDetails": {
          "visibility": "expanded",
          "display": "active"
        }
      }
    },
    "interfaces": {
      "External::INBOUND::APP_ANDROID_USER": {
        "id": "External::INBOUND::APP_ANDROID_USER",
        "name": "APP_ANDROID_USER",
        "kind": "interface::external",
        "parentId": "su:External::INBOUND",
        "details": [
          {
            "key": "requestType",
            "type": "string",
            "value": "INBOUND"
          },
          {
            "key": "clientId",
            "type": "string",
            "value": "APP_ANDROID_USER"
          }
        ],
        "uiDetails": {
          "visibility": "collapsed",
          "display": "active"
        }
      },
      "Tix-Tyrion::Mongo::find": {
        "id": "Tix-Tyrion::Mongo::find",
        "name": "find",
        "kind": "interface::read",
        "parentId": "su:Tix-Tyrion::Mongo",
        "details": [
          {
            "key": "server",
            "type": "string",
            "value": "tix-winterfell-mongodb:27017/tyrion"
          },
          {
            "key": "commandName",
            "type": "string",
            "value": "find"
          }
        ],
        "uiDetails": {
          "visibility": "collapsed",
          "display": "active"
        }
      },
      "Tix-Winterfell::App::GET::/search/movies": {
        "id": "Tix-Winterfell::App::GET::/search/movies",
        "name": "/search/movies",
        "kind": "interface::api",
        "parentId": "su:Tix-Winterfell::App",
        "details": [
          {
            "key": "httpMethod",
            "type": "string",
            "value": "GET"
          },
          {
            "key": "httpRoute",
            "type": "string",
            "value": "/search/movies"
          }
        ],
        "uiDetails": {
          "visibility": "collapsed",
          "display": "active"
        }
      },
      "KAFKA::review_moderation": {
        "id": "KAFKA::review_moderation",
        "name": "review_moderation",
        "kind": "interface::main-queue",
        "parentId": "su:KAFKA::review_moderation",
        "details": [
          {
            "key": "topicName",
            "type": "string",
            "value": "review_moderation"
          }
        ],
        "uiDetails": {
          "visibility": "collapsed",
          "display": "active"
        }
      },
      "Tix-Eyrie-V2::mysql::READ": {
        "id": "Tix-Eyrie-V2::mysql::READ",
        "name": "READ",
        "kind": "interface::read",
        "parentId": "su:Tix-Eyrie-V2::mysql",
        "details": [],
        "uiDetails": {
          "visibility": "collapsed",
          "display": "active"
        }
      },
      "Tix-Winterfell::Mongo::find": {
        "id": "Tix-Winterfell::Mongo::find",
        "name": "find",
        "kind": "interface::read",
        "parentId": "su:Tix-Winterfell::Mongo",
        "details": [
          {
            "key": "server",
            "type": "string",
            "value": "tix-winterfell-mongodb:27017/winterfell"
          },
          {
            "key": "commandName",
            "type": "string",
            "value": "find"
          }
        ],
        "uiDetails": {
          "visibility": "collapsed",
          "display": "active"
        }
      },
      "Tix-Eyrie-V2::App::v2.isUserPastCustomer": {
        "id": "Tix-Eyrie-V2::App::v2.isUserPastCustomer",
        "name": "v2.isUserPastCustomer",
        "kind": "interface::api",
        "parentId": "su:Tix-Eyrie-V2::App",
        "details": [
          {
            "key": "grpcFullMethodName",
            "type": "string",
            "value": "v2.isUserPastCustomer"
          }
        ],
        "uiDetails": {
          "visibility": "collapsed",
          "display": "active"
        }
      },
      "Tix-Winterfell::App::GET::/search/moviesByName": {
        "id": "Tix-Winterfell::App::GET::/search/moviesByName",
        "name": "/search/moviesByName",
        "kind": "interface::api",
        "parentId": "su:Tix-Winterfell::App",
        "details": [
          {
            "key": "httpRoute",
            "type": "string",
            "value": "/search/moviesByName"
          },
          {
            "key": "httpMethod",
            "type": "string",
            "value": "GET"
          }
        ],
        "uiDetails": {
          "visibility": "collapsed",
          "display": "active"
        }
      },
      "Tix-Raven::App::review_moderation-CG_RAVEN": {
        "id": "Tix-Raven::App::review_moderation-CG_RAVEN",
        "name": "review_moderation-CG_RAVEN",
        "kind": "interface::queue-consumer",
        "parentId": "su:Tix-Raven::App",
        "details": [
          {
            "key": "groupId",
            "type": "string",
            "value": "CG_RAVEN"
          },
          {
            "key": "topicName",
            "type": "string",
            "value": "review_moderation"
          }
        ],
        "uiDetails": {
          "visibility": "collapsed",
          "display": "active"
        }
      },
      "Tix-Winterfell::App::POST::/review/edit": {
        "id": "Tix-Winterfell::App::POST::/review/edit",
        "name": "/review/edit",
        "kind": "interface::api",
        "parentId": "su:Tix-Winterfell::App",
        "details": [
          {
            "key": "httpMethod",
            "type": "string",
            "value": "POST"
          },
          {
            "key": "httpRoute",
            "type": "string",
            "value": "/review/edit"
          }
        ],
        "uiDetails": {
          "visibility": "collapsed",
          "display": "active"
        }
      },
      "External::INBOUND::APP_ANDROID_BROWSE": {
        "id": "External::INBOUND::APP_ANDROID_BROWSE",
        "name": "APP_ANDROID_BROWSE",
        "kind": "interface::external",
        "parentId": "su:External::INBOUND",
        "details": [
          {
            "key": "clientId",
            "type": "string",
            "value": "APP_ANDROID_BROWSE"
          },
          {
            "key": "requestType",
            "type": "string",
            "value": "INBOUND"
          }
        ],
        "uiDetails": {
          "visibility": "collapsed",
          "display": "active"
        }
      },
      "Tix-Tyrion::App::review_moderation-CG_INGEST": {
        "id": "Tix-Tyrion::App::review_moderation-CG_INGEST",
        "name": "review_moderation-CG_INGEST",
        "kind": "interface::queue-consumer",
        "parentId": "su:Tix-Tyrion::App",
        "details": [
          {
            "key": "groupId",
            "type": "string",
            "value": "CG_INGEST"
          },
          {
            "key": "topicName",
            "type": "string",
            "value": "review_moderation"
          }
        ],
        "uiDetails": {
          "visibility": "collapsed",
          "display": "active"
        }
      },
      "Tix-Winterfell::App::POST::/review/submit": {
        "id": "Tix-Winterfell::App::POST::/review/submit",
        "name": "/review/submit",
        "kind": "interface::api",
        "parentId": "su:Tix-Winterfell::App",
        "details": [
          {
            "key": "httpRoute",
            "type": "string",
            "value": "/review/submit"
          },
          {
            "key": "httpMethod",
            "type": "string",
            "value": "POST"
          }
        ],
        "uiDetails": {
          "visibility": "collapsed",
          "display": "active"
        }
      },
      "Tix-Tyrion::App::GET::/reviewsForMovie": {
        "id": "Tix-Tyrion::App::GET::/reviewsForMovie",
        "name": "/reviewsForMovie",
        "kind": "interface::api",
        "parentId": "su:Tix-Tyrion::App",
        "details": [
          {
            "key": "httpRoute",
            "type": "string",
            "value": "/reviewsForMovie"
          },
          {
            "key": "httpMethod",
            "type": "string",
            "value": "GET"
          }
        ],
        "uiDetails": {
          "visibility": "collapsed",
          "display": "active"
        }
      },
      "Tix-Tyrion::Mongo::aggregate": {
        "id": "Tix-Tyrion::Mongo::aggregate",
        "name": "aggregate",
        "kind": "interface::read",
        "parentId": "su:Tix-Tyrion::Mongo",
        "details": [
          {
            "key": "commandName",
            "type": "string",
            "value": "aggregate"
          },
          {
            "key": "server",
            "type": "string",
            "value": "tix-winterfell-mongodb:27017/tyrion"
          }
        ],
        "uiDetails": {
          "visibility": "collapsed",
          "display": "active"
        }
      },
      "Tix-Tyrion::Mongo::update": {
        "id": "Tix-Tyrion::Mongo::update",
        "name": "update",
        "kind": "interface::read",
        "parentId": "su:Tix-Tyrion::Mongo",
        "details": [
          {
            "key": "server",
            "type": "string",
            "value": "tix-winterfell-mongodb:27017/tyrion"
          },
          {
            "key": "commandName",
            "type": "string",
            "value": "update"
          }
        ],
        "uiDetails": {
          "visibility": "collapsed",
          "display": "active"
        }
      }
    },
    "edges": {
      "ss_in:ss:KAFKA::review_moderation->Tix-Tyrion::App::review_moderation-CG_INGEST": {
        "id": "ss_in:ss:KAFKA::review_moderation->Tix-Tyrion::App::review_moderation-CG_INGEST",
        "kind": "EDGE_ASYNC",
        "edgeType": "SS_IN_EDGE",
        "sourceId": "ss:KAFKA::review_moderation",
        "targetId": "Tix-Tyrion::App::review_moderation-CG_INGEST"
      },
      "in_ss:Tix-Winterfell::App::POST::/review/submit->ss:KAFKA::review_moderation": {
        "id": "in_ss:Tix-Winterfell::App::POST::/review/submit->ss:KAFKA::review_moderation",
        "kind": "EDGE_SYNC",
        "edgeType": "IN_SS_EDGE",
        "sourceId": "Tix-Winterfell::App::POST::/review/submit",
        "targetId": "ss:KAFKA::review_moderation"
      },
      "in_in:Tix-Winterfell::App::POST::/review/edit->KAFKA::review_moderation": {
        "id": "in_in:Tix-Winterfell::App::POST::/review/edit->KAFKA::review_moderation",
        "kind": "EDGE_SYNC",
        "edgeType": "IN_IN_EDGE",
        "sourceId": "Tix-Winterfell::App::POST::/review/edit",
        "targetId": "KAFKA::review_moderation"
      },
      "in_in:Tix-Winterfell::App::POST::/review/submit->KAFKA::review_moderation": {
        "id": "in_in:Tix-Winterfell::App::POST::/review/submit->KAFKA::review_moderation",
        "kind": "EDGE_SYNC",
        "edgeType": "IN_IN_EDGE",
        "sourceId": "Tix-Winterfell::App::POST::/review/submit",
        "targetId": "KAFKA::review_moderation"
      },
      "su_su:su:Tix-Winterfell::App->su:Tix-Winterfell::Mongo": {
        "id": "su_su:su:Tix-Winterfell::App->su:Tix-Winterfell::Mongo",
        "kind": "EDGE_SYNC",
        "edgeType": "SU_SU_EDGE",
        "sourceId": "su:Tix-Winterfell::App",
        "targetId": "su:Tix-Winterfell::Mongo"
      },
      "in_in:KAFKA::review_moderation->Tix-Tyrion::App::review_moderation-CG_INGEST": {
        "id": "in_in:KAFKA::review_moderation->Tix-Tyrion::App::review_moderation-CG_INGEST",
        "kind": "EDGE_ASYNC",
        "edgeType": "IN_IN_EDGE",
        "sourceId": "KAFKA::review_moderation",
        "targetId": "Tix-Tyrion::App::review_moderation-CG_INGEST"
      },
      "in_ss:Tix-Winterfell::App::GET::/search/moviesByName->ss:Tix-Tyrion": {
        "id": "in_ss:Tix-Winterfell::App::GET::/search/moviesByName->ss:Tix-Tyrion",
        "kind": "EDGE_SYNC",
        "edgeType": "IN_SS_EDGE",
        "sourceId": "Tix-Winterfell::App::GET::/search/moviesByName",
        "targetId": "ss:Tix-Tyrion"
      },
      "ss_ss:ss:Tix-Raven->ss:Tix-Eyrie-V2": {
        "id": "ss_ss:ss:Tix-Raven->ss:Tix-Eyrie-V2",
        "kind": "EDGE_SYNC",
        "edgeType": "SS_SS_EDGE",
        "sourceId": "ss:Tix-Raven",
        "targetId": "ss:Tix-Eyrie-V2"
      },
      "ss_ss:ss:KAFKA::review_moderation->ss:Tix-Raven": {
        "id": "ss_ss:ss:KAFKA::review_moderation->ss:Tix-Raven",
        "kind": "EDGE_ASYNC",
        "edgeType": "SS_SS_EDGE",
        "sourceId": "ss:KAFKA::review_moderation",
        "targetId": "ss:Tix-Raven"
      },
      "in_ss:Tix-Raven::App::review_moderation-CG_RAVEN->ss:Tix-Eyrie-V2": {
        "id": "in_ss:Tix-Raven::App::review_moderation-CG_RAVEN->ss:Tix-Eyrie-V2",
        "kind": "EDGE_SYNC",
        "edgeType": "IN_SS_EDGE",
        "sourceId": "Tix-Raven::App::review_moderation-CG_RAVEN",
        "targetId": "ss:Tix-Eyrie-V2"
      },
      "in_in:KAFKA::review_moderation->Tix-Raven::App::review_moderation-CG_RAVEN": {
        "id": "in_in:KAFKA::review_moderation->Tix-Raven::App::review_moderation-CG_RAVEN",
        "kind": "EDGE_ASYNC",
        "edgeType": "IN_IN_EDGE",
        "sourceId": "KAFKA::review_moderation",
        "targetId": "Tix-Raven::App::review_moderation-CG_RAVEN"
      },
      "in_ss:Tix-Winterfell::App::POST::/review/edit->ss:KAFKA::review_moderation": {
        "id": "in_ss:Tix-Winterfell::App::POST::/review/edit->ss:KAFKA::review_moderation",
        "kind": "EDGE_SYNC",
        "edgeType": "IN_SS_EDGE",
        "sourceId": "Tix-Winterfell::App::POST::/review/edit",
        "targetId": "ss:KAFKA::review_moderation"
      },
      "in_in:External::INBOUND::APP_ANDROID_BROWSE->Tix-Winterfell::App::GET::/search/movies": {
        "id": "in_in:External::INBOUND::APP_ANDROID_BROWSE->Tix-Winterfell::App::GET::/search/movies",
        "kind": "EDGE_SYNC",
        "edgeType": "IN_IN_EDGE",
        "sourceId": "External::INBOUND::APP_ANDROID_BROWSE",
        "targetId": "Tix-Winterfell::App::GET::/search/movies"
      },
      "ss_in:ss:KAFKA::review_moderation->Tix-Raven::App::review_moderation-CG_RAVEN": {
        "id": "ss_in:ss:KAFKA::review_moderation->Tix-Raven::App::review_moderation-CG_RAVEN",
        "kind": "EDGE_ASYNC",
        "edgeType": "SS_IN_EDGE",
        "sourceId": "ss:KAFKA::review_moderation",
        "targetId": "Tix-Raven::App::review_moderation-CG_RAVEN"
      },
      "in_in:Tix-Raven::App::review_moderation-CG_RAVEN->Tix-Eyrie-V2::App::v2.isUserPastCustomer": {
        "id": "in_in:Tix-Raven::App::review_moderation-CG_RAVEN->Tix-Eyrie-V2::App::v2.isUserPastCustomer",
        "kind": "EDGE_SYNC",
        "edgeType": "IN_IN_EDGE",
        "sourceId": "Tix-Raven::App::review_moderation-CG_RAVEN",
        "targetId": "Tix-Eyrie-V2::App::v2.isUserPastCustomer"
      },
      "in_in:Tix-Tyrion::App::review_moderation-CG_INGEST->Tix-Tyrion::Mongo::update": {
        "id": "in_in:Tix-Tyrion::App::review_moderation-CG_INGEST->Tix-Tyrion::Mongo::update",
        "kind": "EDGE_SYNC",
        "edgeType": "IN_IN_EDGE",
        "sourceId": "Tix-Tyrion::App::review_moderation-CG_INGEST",
        "targetId": "Tix-Tyrion::Mongo::update"
      },
      "ss_in:ss:External::INBOUND->Tix-Winterfell::App::GET::/search/movies": {
        "id": "ss_in:ss:External::INBOUND->Tix-Winterfell::App::GET::/search/movies",
        "kind": "EDGE_SYNC",
        "edgeType": "SS_IN_EDGE",
        "sourceId": "ss:External::INBOUND",
        "targetId": "Tix-Winterfell::App::GET::/search/movies"
      },
      "in_in:External::INBOUND::APP_ANDROID_BROWSE->Tix-Winterfell::App::GET::/search/moviesByName": {
        "id": "in_in:External::INBOUND::APP_ANDROID_BROWSE->Tix-Winterfell::App::GET::/search/moviesByName",
        "kind": "EDGE_SYNC",
        "edgeType": "IN_IN_EDGE",
        "sourceId": "External::INBOUND::APP_ANDROID_BROWSE",
        "targetId": "Tix-Winterfell::App::GET::/search/moviesByName"
      },
      "in_ss:KAFKA::review_moderation->ss:Tix-Tyrion": {
        "id": "in_ss:KAFKA::review_moderation->ss:Tix-Tyrion",
        "kind": "EDGE_ASYNC",
        "edgeType": "IN_SS_EDGE",
        "sourceId": "KAFKA::review_moderation",
        "targetId": "ss:Tix-Tyrion"
      },
      "in_in:Tix-Eyrie-V2::App::v2.isUserPastCustomer->Tix-Eyrie-V2::mysql::READ": {
        "id": "in_in:Tix-Eyrie-V2::App::v2.isUserPastCustomer->Tix-Eyrie-V2::mysql::READ",
        "kind": "EDGE_SYNC",
        "edgeType": "IN_IN_EDGE",
        "sourceId": "Tix-Eyrie-V2::App::v2.isUserPastCustomer",
        "targetId": "Tix-Eyrie-V2::mysql::READ"
      },
      "in_ss:External::INBOUND::APP_ANDROID_BROWSE->ss:Tix-Winterfell": {
        "id": "in_ss:External::INBOUND::APP_ANDROID_BROWSE->ss:Tix-Winterfell",
        "kind": "EDGE_SYNC",
        "edgeType": "IN_SS_EDGE",
        "sourceId": "External::INBOUND::APP_ANDROID_BROWSE",
        "targetId": "ss:Tix-Winterfell"
      },
      "in_in:Tix-Winterfell::App::GET::/search/moviesByName->Tix-Tyrion::App::GET::/reviewsForMovie": {
        "id": "in_in:Tix-Winterfell::App::GET::/search/moviesByName->Tix-Tyrion::App::GET::/reviewsForMovie",
        "kind": "EDGE_SYNC",
        "edgeType": "IN_IN_EDGE",
        "sourceId": "Tix-Winterfell::App::GET::/search/moviesByName",
        "targetId": "Tix-Tyrion::App::GET::/reviewsForMovie"
      },
      "in_ss:External::INBOUND::APP_ANDROID_USER->ss:Tix-Winterfell": {
        "id": "in_ss:External::INBOUND::APP_ANDROID_USER->ss:Tix-Winterfell",
        "kind": "EDGE_SYNC",
        "edgeType": "IN_SS_EDGE",
        "sourceId": "External::INBOUND::APP_ANDROID_USER",
        "targetId": "ss:Tix-Winterfell"
      },
      "ss_ss:ss:KAFKA::review_moderation->ss:Tix-Tyrion": {
        "id": "ss_ss:ss:KAFKA::review_moderation->ss:Tix-Tyrion",
        "kind": "EDGE_ASYNC",
        "edgeType": "SS_SS_EDGE",
        "sourceId": "ss:KAFKA::review_moderation",
        "targetId": "ss:Tix-Tyrion"
      },
      "ss_in:ss:External::INBOUND->Tix-Winterfell::App::POST::/review/edit": {
        "id": "ss_in:ss:External::INBOUND->Tix-Winterfell::App::POST::/review/edit",
        "kind": "EDGE_SYNC",
        "edgeType": "SS_IN_EDGE",
        "sourceId": "ss:External::INBOUND",
        "targetId": "Tix-Winterfell::App::POST::/review/edit"
      },
      "in_in:Tix-Winterfell::App::GET::/search/moviesByName->Tix-Winterfell::Mongo::find": {
        "id": "in_in:Tix-Winterfell::App::GET::/search/moviesByName->Tix-Winterfell::Mongo::find",
        "kind": "EDGE_SYNC",
        "edgeType": "IN_IN_EDGE",
        "sourceId": "Tix-Winterfell::App::GET::/search/moviesByName",
        "targetId": "Tix-Winterfell::Mongo::find"
      },
      "in_in:External::INBOUND::APP_ANDROID_USER->Tix-Winterfell::App::POST::/review/submit": {
        "id": "in_in:External::INBOUND::APP_ANDROID_USER->Tix-Winterfell::App::POST::/review/submit",
        "kind": "EDGE_SYNC",
        "edgeType": "IN_IN_EDGE",
        "sourceId": "External::INBOUND::APP_ANDROID_USER",
        "targetId": "Tix-Winterfell::App::POST::/review/submit"
      },
      "ss_in:ss:External::INBOUND->Tix-Winterfell::App::POST::/review/submit": {
        "id": "ss_in:ss:External::INBOUND->Tix-Winterfell::App::POST::/review/submit",
        "kind": "EDGE_SYNC",
        "edgeType": "SS_IN_EDGE",
        "sourceId": "ss:External::INBOUND",
        "targetId": "Tix-Winterfell::App::POST::/review/submit"
      },
      "in_ss:KAFKA::review_moderation->ss:Tix-Raven": {
        "id": "in_ss:KAFKA::review_moderation->ss:Tix-Raven",
        "kind": "EDGE_ASYNC",
        "edgeType": "IN_SS_EDGE",
        "sourceId": "KAFKA::review_moderation",
        "targetId": "ss:Tix-Raven"
      },
      "ss_ss:ss:Tix-Winterfell->ss:Tix-Tyrion": {
        "id": "ss_ss:ss:Tix-Winterfell->ss:Tix-Tyrion",
        "kind": "EDGE_SYNC",
        "edgeType": "SS_SS_EDGE",
        "sourceId": "ss:Tix-Winterfell",
        "targetId": "ss:Tix-Tyrion"
      },
      "su_su:su:Tix-Tyrion::App->su:Tix-Tyrion::Mongo": {
        "id": "su_su:su:Tix-Tyrion::App->su:Tix-Tyrion::Mongo",
        "kind": "EDGE_SYNC",
        "edgeType": "SU_SU_EDGE",
        "sourceId": "su:Tix-Tyrion::App",
        "targetId": "su:Tix-Tyrion::Mongo"
      },
      "ss_in:ss:Tix-Raven->Tix-Eyrie-V2::App::v2.isUserPastCustomer": {
        "id": "ss_in:ss:Tix-Raven->Tix-Eyrie-V2::App::v2.isUserPastCustomer",
        "kind": "EDGE_SYNC",
        "edgeType": "SS_IN_EDGE",
        "sourceId": "ss:Tix-Raven",
        "targetId": "Tix-Eyrie-V2::App::v2.isUserPastCustomer"
      },
      "ss_in:ss:External::INBOUND->Tix-Winterfell::App::GET::/search/moviesByName": {
        "id": "ss_in:ss:External::INBOUND->Tix-Winterfell::App::GET::/search/moviesByName",
        "kind": "EDGE_SYNC",
        "edgeType": "SS_IN_EDGE",
        "sourceId": "ss:External::INBOUND",
        "targetId": "Tix-Winterfell::App::GET::/search/moviesByName"
      },
      "in_in:External::INBOUND::APP_ANDROID_USER->Tix-Winterfell::App::POST::/review/edit": {
        "id": "in_in:External::INBOUND::APP_ANDROID_USER->Tix-Winterfell::App::POST::/review/edit",
        "kind": "EDGE_SYNC",
        "edgeType": "IN_IN_EDGE",
        "sourceId": "External::INBOUND::APP_ANDROID_USER",
        "targetId": "Tix-Winterfell::App::POST::/review/edit"
      },
      "ss_ss:ss:External::INBOUND->ss:Tix-Winterfell": {
        "id": "ss_ss:ss:External::INBOUND->ss:Tix-Winterfell",
        "kind": "EDGE_SYNC",
        "edgeType": "SS_SS_EDGE",
        "sourceId": "ss:External::INBOUND",
        "targetId": "ss:Tix-Winterfell"
      },
      "ss_in:ss:Tix-Winterfell->Tix-Tyrion::App::GET::/reviewsForMovie": {
        "id": "ss_in:ss:Tix-Winterfell->Tix-Tyrion::App::GET::/reviewsForMovie",
        "kind": "EDGE_SYNC",
        "edgeType": "SS_IN_EDGE",
        "sourceId": "ss:Tix-Winterfell",
        "targetId": "Tix-Tyrion::App::GET::/reviewsForMovie"
      },
      "ss_ss:ss:Tix-Winterfell->ss:KAFKA::review_moderation": {
        "id": "ss_ss:ss:Tix-Winterfell->ss:KAFKA::review_moderation",
        "kind": "EDGE_SYNC",
        "edgeType": "SS_SS_EDGE",
        "sourceId": "ss:Tix-Winterfell",
        "targetId": "ss:KAFKA::review_moderation"
      },
      "in_in:Tix-Tyrion::App::GET::/reviewsForMovie->Tix-Tyrion::Mongo::find": {
        "id": "in_in:Tix-Tyrion::App::GET::/reviewsForMovie->Tix-Tyrion::Mongo::find",
        "kind": "EDGE_SYNC",
        "edgeType": "IN_IN_EDGE",
        "sourceId": "Tix-Tyrion::App::GET::/reviewsForMovie",
        "targetId": "Tix-Tyrion::Mongo::find"
      },
      "ss_in:ss:Tix-Winterfell->KAFKA::review_moderation": {
        "id": "ss_in:ss:Tix-Winterfell->KAFKA::review_moderation",
        "kind": "EDGE_SYNC",
        "edgeType": "SS_IN_EDGE",
        "sourceId": "ss:Tix-Winterfell",
        "targetId": "KAFKA::review_moderation"
      },
      "su_su:su:Tix-Eyrie-V2::App->su:Tix-Eyrie-V2::mysql": {
        "id": "su_su:su:Tix-Eyrie-V2::App->su:Tix-Eyrie-V2::mysql",
        "kind": "EDGE_SYNC",
        "edgeType": "SU_SU_EDGE",
        "sourceId": "su:Tix-Eyrie-V2::App",
        "targetId": "su:Tix-Eyrie-V2::mysql"
      },
      "in_in:Tix-Tyrion::App::GET::/reviewsForMovie->Tix-Tyrion::Mongo::aggregate": {
        "id": "in_in:Tix-Tyrion::App::GET::/reviewsForMovie->Tix-Tyrion::Mongo::aggregate",
        "kind": "EDGE_SYNC",
        "edgeType": "IN_IN_EDGE",
        "sourceId": "Tix-Tyrion::App::GET::/reviewsForMovie",
        "targetId": "Tix-Tyrion::Mongo::aggregate"
      }
    }
  },
  "baseTimelineGraph": {
    "interfaces": [
      "External::INBOUND::APP_ANDROID_USER",
      "Tix-Tyrion::Mongo::find",
      "Tix-Winterfell::App::GET::/search/movies",
      "KAFKA::review_moderation",
      "Tix-Eyrie-V2::mysql::READ",
      "Tix-Winterfell::Mongo::find",
      "Tix-Eyrie-V2::App::v2.isUserPastCustomer",
      "Tix-Winterfell::App::GET::/search/moviesByName",
      "Tix-Raven::App::review_moderation-CG_RAVEN",
      "Tix-Winterfell::App::POST::/review/edit",
      "External::INBOUND::APP_ANDROID_BROWSE",
      "Tix-Tyrion::App::review_moderation-CG_INGEST",
      "Tix-Winterfell::App::POST::/review/submit",
      "Tix-Tyrion::App::GET::/reviewsForMovie",
      "Tix-Tyrion::Mongo::aggregate",
      "Tix-Tyrion::Mongo::update"
    ],
    "systemunits": [
      "su:Tix-Eyrie-V2::App",
      "su:Tix-Raven::App",
      "su:KAFKA::review_moderation",
      "su:Tix-Tyrion::Mongo",
      "su:External::INBOUND",
      "su:Tix-Winterfell::App",
      "su:Tix-Winterfell::Mongo",
      "su:Tix-Eyrie-V2::mysql",
      "su:Tix-Tyrion::App"
    ],
    "subsystems": [
      "ss:Tix-Tyrion",
      "ss:Tix-Raven",
      "ss:External::INBOUND",
      "ss:Tix-Winterfell",
      "ss:KAFKA::review_moderation",
      "ss:Tix-Eyrie-V2"
    ],
    "edges": [
      "ss_in:ss:KAFKA::review_moderation->Tix-Tyrion::App::review_moderation-CG_INGEST",
      "in_ss:Tix-Winterfell::App::POST::/review/submit->ss:KAFKA::review_moderation",
      "in_in:Tix-Winterfell::App::POST::/review/edit->KAFKA::review_moderation",
      "in_in:Tix-Winterfell::App::POST::/review/submit->KAFKA::review_moderation",
      "su_su:su:Tix-Winterfell::App->su:Tix-Winterfell::Mongo",
      "in_in:KAFKA::review_moderation->Tix-Tyrion::App::review_moderation-CG_INGEST",
      "in_ss:Tix-Winterfell::App::GET::/search/moviesByName->ss:Tix-Tyrion",
      "ss_ss:ss:Tix-Raven->ss:Tix-Eyrie-V2",
      "ss_ss:ss:KAFKA::review_moderation->ss:Tix-Raven",
      "in_ss:Tix-Raven::App::review_moderation-CG_RAVEN->ss:Tix-Eyrie-V2",
      "in_in:KAFKA::review_moderation->Tix-Raven::App::review_moderation-CG_RAVEN",
      "in_ss:Tix-Winterfell::App::POST::/review/edit->ss:KAFKA::review_moderation",
      "in_in:External::INBOUND::APP_ANDROID_BROWSE->Tix-Winterfell::App::GET::/search/movies",
      "ss_in:ss:KAFKA::review_moderation->Tix-Raven::App::review_moderation-CG_RAVEN",
      "in_in:Tix-Raven::App::review_moderation-CG_RAVEN->Tix-Eyrie-V2::App::v2.isUserPastCustomer",
      "in_in:Tix-Tyrion::App::review_moderation-CG_INGEST->Tix-Tyrion::Mongo::update",
      "ss_in:ss:External::INBOUND->Tix-Winterfell::App::GET::/search/movies",
      "in_in:External::INBOUND::APP_ANDROID_BROWSE->Tix-Winterfell::App::GET::/search/moviesByName",
      "in_ss:KAFKA::review_moderation->ss:Tix-Tyrion",
      "in_in:Tix-Eyrie-V2::App::v2.isUserPastCustomer->Tix-Eyrie-V2::mysql::READ",
      "in_ss:External::INBOUND::APP_ANDROID_BROWSE->ss:Tix-Winterfell",
      "in_in:Tix-Winterfell::App::GET::/search/moviesByName->Tix-Tyrion::App::GET::/reviewsForMovie",
      "in_ss:External::INBOUND::APP_ANDROID_USER->ss:Tix-Winterfell",
      "ss_ss:ss:KAFKA::review_moderation->ss:Tix-Tyrion",
      "ss_in:ss:External::INBOUND->Tix-Winterfell::App::POST::/review/edit",
      "in_in:Tix-Winterfell::App::GET::/search/moviesByName->Tix-Winterfell::Mongo::find",
      "in_in:External::INBOUND::APP_ANDROID_USER->Tix-Winterfell::App::POST::/review/submit",
      "ss_in:ss:External::INBOUND->Tix-Winterfell::App::POST::/review/submit",
      "in_ss:KAFKA::review_moderation->ss:Tix-Raven",
      "ss_ss:ss:Tix-Winterfell->ss:Tix-Tyrion",
      "su_su:su:Tix-Tyrion::App->su:Tix-Tyrion::Mongo",
      "ss_in:ss:Tix-Raven->Tix-Eyrie-V2::App::v2.isUserPastCustomer",
      "ss_in:ss:External::INBOUND->Tix-Winterfell::App::GET::/search/moviesByName",
      "in_in:External::INBOUND::APP_ANDROID_USER->Tix-Winterfell::App::POST::/review/edit",
      "ss_ss:ss:External::INBOUND->ss:Tix-Winterfell",
      "ss_in:ss:Tix-Winterfell->Tix-Tyrion::App::GET::/reviewsForMovie",
      "ss_ss:ss:Tix-Winterfell->ss:KAFKA::review_moderation",
      "in_in:Tix-Tyrion::App::GET::/reviewsForMovie->Tix-Tyrion::Mongo::find",
      "ss_in:ss:Tix-Winterfell->KAFKA::review_moderation",
      "su_su:su:Tix-Eyrie-V2::App->su:Tix-Eyrie-V2::mysql",
      "in_in:Tix-Tyrion::App::GET::/reviewsForMovie->Tix-Tyrion::Mongo::aggregate"
    ]
  }
}





API 2
curl -X 'POST' \
  'http://localhost:8081/demo/ui/graph-paths/details/pinned?version=demo--595&nodeId=Tix-Winterfell%3A%3AApp%3A%3APOST%3A%3A%2Freview%2Fedit' \
  -H 'accept: */*' \
  -d ''

This is to get a detailed view of a particular API/interface.. the response is the same as the graphPaths/all api.. 



API 3 to get the metrics. Latency, throughput and errors.

curl -X 'GET' \
  'http://localhost:8081/demo/ui/graph-paths/overlays/v2?version=demo--595--Tix-Winterfell%3A%3AApp%3A%3APOST%3A%3A%2Freview%2Fedit&epochStartTime=1758371290&epochEndTime=1758371290&uom=qpm' \
  -H 'accept: */*'

  Response.
  {
  "uomData": {
    "t": "qpm",
    "e": "pc",
    "l": "ms"
  },
  "tickResponse": {
    "demo--595": {
      "edges": {
        "ss_in:ss:KAFKA::review_moderation->Tix-Tyrion::App::review_moderation-CG_INGEST": {
          "server_metrics": {
            "t": {
              "qpm": 1950
            },
            "e": {
              "total": 0,
              "4xx": 0,
              "5xx": 0
            },
            "l": {
              "0.5": 85.6531452535265,
              "0.99": 239.82295081967214,
              "0.9": 154.16980556614564,
              "0.95": 188.44277544796034
            }
          }
        },
        "in_ss:Tix-Winterfell::App::POST::/review/submit->ss:KAFKA::review_moderation": {
          "server_metrics": {
            "t": {
              "qpm": 1500
            },
            "e": {
              "total": 0,
              "4xx": 0,
              "5xx": 0
            },
            "l": {
              "0.5": 5.3,
              "0.99": 14.9,
              "0.9": 9.6,
              "0.95": 11.7
            }
          }
        },
        "in_in:Tix-Winterfell::App::POST::/review/edit->KAFKA::review_moderation": {
          "server_metrics": {
            "t": {
              "qpm": 450
            },
            "e": {
              "total": 0,
              "4xx": 0,
              "5xx": 0
            },
            "l": {
              "0.5": 5.4,
              "0.99": 15.2,
              "0.9": 9.8,
              "0.95": 12
            }
          }
        },
        "in_in:Tix-Winterfell::App::POST::/review/submit->KAFKA::review_moderation": {
          "server_metrics": {
            "t": {
              "qpm": 1500
            },
            "e": {
              "total": 0,
              "4xx": 0,
              "5xx": 0
            },
            "l": {
              "0.5": 5.3,
              "0.99": 14.9,
              "0.9": 9.6,
              "0.95": 11.7
            }
          }
        },
        "in_in:KAFKA::review_moderation->Tix-Tyrion::App::review_moderation-CG_INGEST": {
          "server_metrics": {
            "t": {
              "qpm": 1950
            },
            "e": {
              "total": 0,
              "4xx": 0,
              "5xx": 0
            },
            "l": {
              "0.5": 85.6531452535265,
              "0.99": 239.82295081967214,
              "0.9": 154.16980556614564,
              "0.95": 188.44277544796034
            }
          }
        },
        "in_ss:Tix-Winterfell::App::GET::/search/moviesByName->ss:Tix-Tyrion": {
          "server_metrics": {
            "t": {
              "qpm": 772.7
            },
            "e": {
              "total": 5.700000000000001,
              "4xx": 4,
              "5xx": 1.7000000000000002
            },
            "l": {
              "0.5": 180.6,
              "0.99": 505.6,
              "0.9": 325,
              "0.95": 397.2
            }
          }
        },
        "ss_ss:ss:Tix-Raven->ss:Tix-Eyrie-V2": {
          "server_metrics": {
            "t": {
              "qpm": 1500
            },
            "e": {
              "total": 0,
              "4xx": 0,
              "5xx": 0
            },
            "l": {
              "0.5": 69.3,
              "0.99": 194,
              "0.9": 124.7,
              "0.95": 152.4
            }
          }
        },
        "ss_ss:ss:KAFKA::review_moderation->ss:Tix-Raven": {
          "server_metrics": {
            "t": {
              "qpm": 1950
            },
            "e": {
              "total": 0,
              "4xx": 0,
              "5xx": 0
            },
            "l": {
              "0.5": 58.502825732199604,
              "0.99": 163.857064330499,
              "0.9": 105.3542385982994,
              "0.95": 128.7799450313493
            }
          }
        },
        "in_in:KAFKA::review_moderation->Tix-Raven::App::review_moderation-CG_RAVEN": {
          "server_metrics": {
            "t": {
              "qpm": 1950
            },
            "e": {
              "total": 0,
              "4xx": 0,
              "5xx": 0
            },
            "l": {
              "0.5": 58.502825732199604,
              "0.99": 163.857064330499,
              "0.9": 105.3542385982994,
              "0.95": 128.7799450313493
            }
          }
        },
        "in_ss:Tix-Raven::App::review_moderation-CG_RAVEN->ss:Tix-Eyrie-V2": {
          "server_metrics": {
            "t": {
              "qpm": 1500
            },
            "e": {
              "total": 0,
              "4xx": 0,
              "5xx": 0
            },
            "l": {
              "0.5": 69.3,
              "0.99": 194,
              "0.9": 124.7,
              "0.95": 152.4
            }
          }
        },
        "in_ss:Tix-Winterfell::App::POST::/review/edit->ss:KAFKA::review_moderation": {
          "server_metrics": {
            "t": {
              "qpm": 450
            },
            "e": {
              "total": 0,
              "4xx": 0,
              "5xx": 0
            },
            "l": {
              "0.5": 5.4,
              "0.99": 15.2,
              "0.9": 9.8,
              "0.95": 12
            }
          }
        },
        "in_in:External::INBOUND::APP_ANDROID_BROWSE->Tix-Winterfell::App::GET::/search/movies": {
          "server_metrics": {
            "t": {
              "qpm": 367.4
            },
            "e": {
              "total": 0,
              "4xx": 0,
              "5xx": 0
            },
            "l": {
              "0.5": 67.3,
              "0.99": 188.5,
              "0.9": 121.2,
              "0.95": 148.1
            }
          }
        },
        "ss_in:ss:KAFKA::review_moderation->Tix-Raven::App::review_moderation-CG_RAVEN": {
          "server_metrics": {
            "t": {
              "qpm": 1950
            },
            "e": {
              "total": 0,
              "4xx": 0,
              "5xx": 0
            },
            "l": {
              "0.5": 58.502825732199604,
              "0.99": 163.857064330499,
              "0.9": 105.3542385982994,
              "0.95": 128.7799450313493
            }
          }
        },
        "in_in:Tix-Raven::App::review_moderation-CG_RAVEN->Tix-Eyrie-V2::App::v2.isUserPastCustomer": {
          "server_metrics": {
            "t": {
              "qpm": 1500
            },
            "e": {
              "total": 0,
              "4xx": 0,
              "5xx": 0
            },
            "l": {
              "0.5": 69.3,
              "0.99": 194,
              "0.9": 124.7,
              "0.95": 152.4
            }
          }
        },
        "in_in:Tix-Tyrion::App::review_moderation-CG_INGEST->Tix-Tyrion::Mongo::update": {
          "server_metrics": {
            "t": {
              "qpm": 1950
            },
            "e": {
              "total": 0,
              "4xx": 0,
              "5xx": 0
            },
            "l": {
              "0.5": 50.01086510865109,
              "0.99": 140.01405142622855,
              "0.9": 90.00318631757746,
              "0.95": 110.0402741170269
            }
          }
        },
        "ss_in:ss:External::INBOUND->Tix-Winterfell::App::GET::/search/movies": {
          "server_metrics": {
            "t": {
              "qpm": 367.4
            },
            "e": {
              "total": 0,
              "4xx": 0,
              "5xx": 0
            },
            "l": {
              "0.5": 67.3,
              "0.99": 188.5,
              "0.9": 121.2,
              "0.95": 148.1
            }
          }
        },
        "in_in:External::INBOUND::APP_ANDROID_BROWSE->Tix-Winterfell::App::GET::/search/moviesByName": {
          "server_metrics": {
            "t": {
              "qpm": 772.7
            },
            "e": {
              "total": 6,
              "4xx": 4.2,
              "5xx": 1.7999999999999998
            },
            "l": {
              "0.5": 244.1,
              "0.99": 683.4,
              "0.9": 439.3,
              "0.95": 536.9
            }
          }
        },
        "in_ss:KAFKA::review_moderation->ss:Tix-Tyrion": {
          "server_metrics": {
            "t": {
              "qpm": 1950
            },
            "e": {
              "total": 0,
              "4xx": 0,
              "5xx": 0
            },
            "l": {
              "0.5": 85.6531452535265,
              "0.99": 239.82295081967214,
              "0.9": 154.16980556614564,
              "0.95": 188.44277544796034
            }
          }
        },
        "in_in:Tix-Eyrie-V2::App::v2.isUserPastCustomer->Tix-Eyrie-V2::mysql::READ": {
          "server_metrics": {
            "t": {
              "qpm": 3000
            },
            "e": {
              "total": 0,
              "4xx": 0,
              "5xx": 0
            },
            "l": {
              "0.5": 21.2,
              "0.99": 59.4,
              "0.9": 38.2,
              "0.95": 46.7
            }
          }
        },
        "in_ss:External::INBOUND::APP_ANDROID_BROWSE->ss:Tix-Winterfell": {
          "server_metrics": {
            "t": {
              "qpm": 1140.1
            },
            "e": {
              "total": 2.7420543317244164,
              "4xx": 1.9194380322070912,
              "5xx": 0.8226162995173248
            },
            "l": {
              "0.5": 186.51724994355385,
              "0.99": 522.2138970422217,
              "0.9": 335.6966470986679,
              "0.95": 410.2700609618424
            }
          }
        },
        "in_in:Tix-Winterfell::App::GET::/search/moviesByName->Tix-Tyrion::App::GET::/reviewsForMovie": {
          "server_metrics": {
            "t": {
              "qpm": 772.7
            },
            "e": {
              "total": 5.700000000000001,
              "4xx": 4,
              "5xx": 1.7000000000000002
            },
            "l": {
              "0.5": 180.6,
              "0.99": 505.6,
              "0.9": 325,
              "0.95": 397.2
            }
          }
        },
        "in_ss:External::INBOUND::APP_ANDROID_USER->ss:Tix-Winterfell": {
          "server_metrics": {
            "t": {
              "qpm": 1950
            },
            "e": {
              "total": 0,
              "4xx": 0,
              "5xx": 0
            },
            "l": {
              "0.5": 39.874927255092146,
              "0.99": 111.709796314258,
              "0.9": 71.83486905916585,
              "0.95": 87.76483996120271
            }
          }
        },
        "ss_ss:ss:KAFKA::review_moderation->ss:Tix-Tyrion": {
          "server_metrics": {
            "t": {
              "qpm": 1950
            },
            "e": {
              "total": 0,
              "4xx": 0,
              "5xx": 0
            },
            "l": {
              "0.5": 85.6531452535265,
              "0.99": 239.82295081967214,
              "0.9": 154.16980556614564,
              "0.95": 188.44277544796034
            }
          }
        },
        "ss_in:ss:External::INBOUND->Tix-Winterfell::App::POST::/review/edit": {
          "server_metrics": {
            "t": {
              "qpm": 450
            },
            "e": {
              "total": 0,
              "4xx": 0,
              "5xx": 0
            },
            "l": {
              "0.5": 43.3,
              "0.99": 121.30000000000001,
              "0.9": 78,
              "0.95": 95.3
            }
          }
        },
        "in_in:Tix-Winterfell::App::GET::/search/moviesByName->Tix-Winterfell::Mongo::find": {
          "server_metrics": {
            "t": {
              "qpm": 772.7
            },
            "e": {
              "total": 0,
              "4xx": 0,
              "5xx": 0
            },
            "l": {
              "0.5": 27.2,
              "0.99": 76.1,
              "0.9": 48.9,
              "0.95": 59.8
            }
          }
        },
        "in_in:External::INBOUND::APP_ANDROID_USER->Tix-Winterfell::App::POST::/review/submit": {
          "server_metrics": {
            "t": {
              "qpm": 1500
            },
            "e": {
              "total": 0,
              "4xx": 0,
              "5xx": 0
            },
            "l": {
              "0.5": 38.8,
              "0.99": 108.7,
              "0.9": 69.89999999999999,
              "0.95": 85.4
            }
          }
        },
        "ss_in:ss:External::INBOUND->Tix-Winterfell::App::POST::/review/submit": {
          "server_metrics": {
            "t": {
              "qpm": 1500
            },
            "e": {
              "total": 0,
              "4xx": 0,
              "5xx": 0
            },
            "l": {
              "0.5": 38.8,
              "0.99": 108.7,
              "0.9": 69.89999999999999,
              "0.95": 85.4
            }
          }
        },
        "in_ss:KAFKA::review_moderation->ss:Tix-Raven": {
          "server_metrics": {
            "t": {
              "qpm": 1950
            },
            "e": {
              "total": 0,
              "4xx": 0,
              "5xx": 0
            },
            "l": {
              "0.5": 58.502825732199604,
              "0.99": 163.857064330499,
              "0.9": 105.3542385982994,
              "0.95": 128.7799450313493
            }
          }
        },
        "ss_ss:ss:Tix-Winterfell->ss:Tix-Tyrion": {
          "server_metrics": {
            "t": {
              "qpm": 772.7
            },
            "e": {
              "total": 5.700000000000001,
              "4xx": 4,
              "5xx": 1.7000000000000002
            },
            "l": {
              "0.5": 180.6,
              "0.99": 505.6,
              "0.9": 325,
              "0.95": 397.2
            }
          }
        },
        "ss_in:ss:Tix-Raven->Tix-Eyrie-V2::App::v2.isUserPastCustomer": {
          "server_metrics": {
            "t": {
              "qpm": 1500
            },
            "e": {
              "total": 0,
              "4xx": 0,
              "5xx": 0
            },
            "l": {
              "0.5": 69.3,
              "0.99": 194,
              "0.9": 124.7,
              "0.95": 152.4
            }
          }
        },
        "ss_in:ss:External::INBOUND->Tix-Winterfell::App::GET::/search/moviesByName": {
          "server_metrics": {
            "t": {
              "qpm": 772.7
            },
            "e": {
              "total": 6,
              "4xx": 4.2,
              "5xx": 1.7999999999999998
            },
            "l": {
              "0.5": 244.1,
              "0.99": 683.4,
              "0.9": 439.3,
              "0.95": 536.9
            }
          }
        },
        "in_in:External::INBOUND::APP_ANDROID_USER->Tix-Winterfell::App::POST::/review/edit": {
          "server_metrics": {
            "t": {
              "qpm": 450
            },
            "e": {
              "total": 0,
              "4xx": 0,
              "5xx": 0
            },
            "l": {
              "0.5": 43.3,
              "0.99": 121.30000000000001,
              "0.9": 78,
              "0.95": 95.3
            }
          }
        },
        "ss_ss:ss:External::INBOUND->ss:Tix-Winterfell": {
          "server_metrics": {
            "t": {
              "qpm": 3090.1
            },
            "e": {
              "total": 0.3268722495809566,
              "4xx": 0.22881057470666957,
              "5xx": 0.09806167487428695
            },
            "l": {
              "0.5": 87.25447548876568,
              "0.99": 244.34203020134225,
              "0.9": 157.0875547125766,
              "0.95": 191.96498759848262
            }
          }
        },
        "ss_in:ss:Tix-Winterfell->Tix-Tyrion::App::GET::/reviewsForMovie": {
          "server_metrics": {
            "t": {
              "qpm": 772.7
            },
            "e": {
              "total": 5.700000000000001,
              "4xx": 4,
              "5xx": 1.7000000000000002
            },
            "l": {
              "0.5": 180.6,
              "0.99": 505.6,
              "0.9": 325,
              "0.95": 397.2
            }
          }
        },
        "in_in:Tix-Tyrion::App::GET::/reviewsForMovie->Tix-Tyrion::Mongo::find": {
          "server_metrics": {
            "t": {
              "qpm": 77.3
            },
            "e": {
              "total": 0,
              "4xx": 0,
              "5xx": 0
            },
            "l": {
              "0.5": 40,
              "0.99": 112,
              "0.9": 72,
              "0.95": 88
            }
          }
        },
        "ss_ss:ss:Tix-Winterfell->ss:KAFKA::review_moderation": {
          "server_metrics": {
            "t": {
              "qpm": 1950
            },
            "e": {
              "total": 0,
              "4xx": 0,
              "5xx": 0
            },
            "l": {
              "0.5": 5.322316384180791,
              "0.99": 14.966949152542373,
              "0.9": 9.644632768361582,
              "0.95": 11.766949152542374
            }
          }
        },
        "ss_in:ss:Tix-Winterfell->KAFKA::review_moderation": {
          "server_metrics": {
            "t": {
              "qpm": 1950
            },
            "e": {
              "total": 0,
              "4xx": 0,
              "5xx": 0
            },
            "l": {
              "0.5": 5.322316384180791,
              "0.99": 14.966949152542373,
              "0.9": 9.644632768361582,
              "0.95": 11.766949152542374
            }
          }
        },
        "in_in:Tix-Tyrion::App::GET::/reviewsForMovie->Tix-Tyrion::Mongo::aggregate": {
          "server_metrics": {
            "t": {
              "qpm": 1545.4
            },
            "e": {
              "total": 3.0000000000000004,
              "4xx": 2.1,
              "5xx": 0.9000000000000001
            },
            "l": {
              "0.5": 70.2,
              "0.99": 196.6,
              "0.9": 126.4,
              "0.95": 154.5
            }
          }
        }
      },
      "interfaces": {
        "Tix-Winterfell::App::GET::/search/movies": {
          "t": {
            "qpm": 367.4
          },
          "e": {
            "total": 0,
            "4xx": 0,
            "5xx": 0
          },
          "l": {
            "0.5": 67.3,
            "0.99": 188.5,
            "0.9": 121.2,
            "0.95": 148.1
          }
        },
        "Tix-Tyrion::Mongo::find": {
          "t": {
            "qpm": 77.3
          },
          "e": {
            "total": 0,
            "4xx": 0,
            "5xx": 0
          },
          "l": {
            "0.5": 40,
            "0.99": 112,
            "0.9": 72,
            "0.95": 88
          }
        },
        "KAFKA::review_moderation": {
          "t": {
            "qpm": 1950
          },
          "e": {
            "total": 0,
            "4xx": 0,
            "5xx": 0
          },
          "l": {
            "0.5": 5.322316384180791,
            "0.99": 14.966949152542373,
            "0.9": 9.644632768361582,
            "0.95": 11.766949152542374
          }
        },
        "Tix-Winterfell::Mongo::find": {
          "t": {
            "qpm": 772.7
          },
          "e": {
            "total": 0,
            "4xx": 0,
            "5xx": 0
          },
          "l": {
            "0.5": 27.2,
            "0.99": 76.1,
            "0.9": 48.9,
            "0.95": 59.8
          }
        },
        "Tix-Eyrie-V2::mysql::READ": {
          "t": {
            "qpm": 3000
          },
          "e": {
            "total": 0,
            "4xx": 0,
            "5xx": 0
          },
          "l": {
            "0.5": 21.2,
            "0.99": 59.4,
            "0.9": 38.2,
            "0.95": 46.7
          }
        },
        "Tix-Eyrie-V2::App::v2.isUserPastCustomer": {
          "t": {
            "qpm": 1500
          },
          "e": {
            "total": 0,
            "4xx": 0,
            "5xx": 0
          },
          "l": {
            "0.5": 69.3,
            "0.99": 194,
            "0.9": 124.7,
            "0.95": 152.4
          }
        },
        "Tix-Raven::App::review_moderation-CG_RAVEN": {
          "t": {
            "qpm": 1950
          },
          "e": {
            "total": 0,
            "4xx": 0,
            "5xx": 0
          },
          "l": {
            "0.5": 58.502825732199604,
            "0.99": 163.857064330499,
            "0.9": 105.3542385982994,
            "0.95": 128.7799450313493
          }
        },
        "Tix-Winterfell::App::GET::/search/moviesByName": {
          "t": {
            "qpm": 772.7
          },
          "e": {
            "total": 6,
            "4xx": 4.2,
            "5xx": 1.7999999999999998
          },
          "l": {
            "0.5": 244.1,
            "0.99": 683.4,
            "0.9": 439.3,
            "0.95": 536.9
          }
        },
        "Tix-Winterfell::App::POST::/review/edit": {
          "t": {
            "qpm": 450
          },
          "e": {
            "total": 0,
            "4xx": 0,
            "5xx": 0
          },
          "l": {
            "0.5": 43.3,
            "0.99": 121.30000000000001,
            "0.9": 78,
            "0.95": 95.3
          }
        },
        "Tix-Tyrion::App::review_moderation-CG_INGEST": {
          "t": {
            "qpm": 1950
          },
          "e": {
            "total": 0,
            "4xx": 0,
            "5xx": 0
          },
          "l": {
            "0.5": 85.6531452535265,
            "0.99": 239.82295081967214,
            "0.9": 154.16980556614564,
            "0.95": 188.44277544796034
          }
        },
        "Tix-Winterfell::App::POST::/review/submit": {
          "t": {
            "qpm": 1500
          },
          "e": {
            "total": 0,
            "4xx": 0,
            "5xx": 0
          },
          "l": {
            "0.5": 38.8,
            "0.99": 108.7,
            "0.9": 69.89999999999999,
            "0.95": 85.4
          }
        },
        "Tix-Tyrion::App::GET::/reviewsForMovie": {
          "t": {
            "qpm": 772.7
          },
          "e": {
            "total": 5.700000000000001,
            "4xx": 4,
            "5xx": 1.7000000000000002
          },
          "l": {
            "0.5": 180.6,
            "0.99": 505.6,
            "0.9": 325,
            "0.95": 397.2
          }
        },
        "Tix-Tyrion::Mongo::update": {
          "t": {
            "qpm": 1950
          },
          "e": {
            "total": 0,
            "4xx": 0,
            "5xx": 0
          },
          "l": {
            "0.5": 50.01086510865109,
            "0.99": 140.01405142622855,
            "0.9": 90.00318631757746,
            "0.95": 110.0402741170269
          }
        },
        "Tix-Tyrion::Mongo::aggregate": {
          "t": {
            "qpm": 1545.4
          },
          "e": {
            "total": 3.0000000000000004,
            "4xx": 2.1,
            "5xx": 0.9000000000000001
          },
          "l": {
            "0.5": 70.2,
            "0.99": 196.6,
            "0.9": 126.4,
            "0.95": 154.5
          }
        }
      },
      "system_units": {
        "su:Tix-Eyrie-V2::App": {
          "t": {
            "qpm": 1500
          },
          "e": {
            "total": 0,
            "4xx": 0,
            "5xx": 0
          },
          "l": {
            "0.5": 69.3,
            "0.99": 194,
            "0.9": 124.7,
            "0.95": 152.4
          }
        },
        "su:Tix-Raven::App": {
          "t": {
            "qpm": 1950
          },
          "e": {
            "total": 0,
            "4xx": 0,
            "5xx": 0
          },
          "l": {
            "0.5": 58.502825732199604,
            "0.99": 163.857064330499,
            "0.9": 105.3542385982994,
            "0.95": 128.7799450313493
          }
        },
        "su:KAFKA::review_moderation": {
          "t": {
            "qpm": 1950
          },
          "e": {
            "total": 0,
            "4xx": 0,
            "5xx": 0
          },
          "l": {
            "0.5": 5.322316384180791,
            "0.99": 14.966949152542373,
            "0.9": 9.644632768361582,
            "0.95": 11.766949152542374
          }
        },
        "su:Tix-Tyrion::Mongo": {
          "t": {
            "qpm": 3572.7
          },
          "e": {
            "total": 0.4615249282073257,
            "4xx": 0.32306744974512785,
            "5xx": 0.1384574784621977
          },
          "l": {
            "0.5": 56.94102517594138,
            "0.99": 159.43895741130382,
            "0.9": 102.4979322353624,
            "0.95": 125.30173402016977
          }
        },
        "su:Tix-Winterfell::Mongo": {
          "t": {
            "qpm": 772.7
          },
          "e": {
            "total": 0,
            "4xx": 0,
            "5xx": 0
          },
          "l": {
            "0.5": 27.2,
            "0.99": 76.1,
            "0.9": 48.9,
            "0.95": 59.8
          }
        },
        "su:Tix-Winterfell::App": {
          "t": {
            "qpm": 3090.1000000000004
          },
          "e": {
            "total": 0.32687224958095656,
            "4xx": 0.22881057470666955,
            "5xx": 0.09806167487428695
          },
          "l": {
            "0.5": 87.25447548876569,
            "0.99": 244.34203020134225,
            "0.9": 157.08755471257658,
            "0.95": 191.96498759848262
          }
        },
        "su:Tix-Tyrion::App": {
          "t": {
            "qpm": 2722.7
          },
          "e": {
            "total": 0.3770524472783573,
            "4xx": 0.2645982086163911,
            "5xx": 0.11245423866196622
          },
          "l": {
            "0.5": 107.78390737383779,
            "0.99": 301.7718028185486,
            "0.9": 193.98789544471083,
            "0.95": 237.10111689374892
          }
        },
        "su:Tix-Eyrie-V2::mysql": {
          "t": {
            "qpm": 3000
          },
          "e": {
            "total": 0,
            "4xx": 0,
            "5xx": 0
          },
          "l": {
            "0.5": 21.2,
            "0.99": 59.4,
            "0.9": 38.2,
            "0.95": 46.7
          }
        }
      }
    }
  }
}