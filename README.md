# coffe_web_api

### Requirements

* Python 3.9.1

* djangorestframework == 3.12.0
* django == 3.1.5

To start server run

`python manage.py runserver`



## Endpoints

### Item endpoins

- /api/
- /api/create-item
- /api/get-item-by-id/\<str:id>/
- /api/get-item-by-name/\<str:name>/
- /api/delete-item-by-id/\<str:id>/
- /api/delete-item-by-name/\<str:name>/
- /api/patch-item-by-name/\<str:name>/
- /api/patch-item-by-id/\<str:id>/

### User endpoins

* /api/auth
* /api/create-manager
* /api/create-barista

### Schedule endpoins

* /api/create-day-schedule
* /api/get-day-schedule-date-by-id/\<str:id>/
* /api/get-day-schedule-date-by-date/\<yyyy:date>/
* /api/get-all-day-schedule
* /api/patch-day-schedule-by-id/\<str:id>/
* /api/patch-day-schedule-by-date/\<yyyy:date>/

### Receipt endpoins

* /api/create-receipt
* /api/get-receipt-by-id/\<str:id>/
* /api/get-receipt-by-date/\<yyyy:date>/
* /api/delete-receipt/\<str:id>/

### Receipt item endpoins

* /api/create-receipt-item
* /api/delete-receipt-item/\<str:id>/
* /api/patch-receipt-item/\<str:id>/
* /api/get-receipt-item/\<str:id>/