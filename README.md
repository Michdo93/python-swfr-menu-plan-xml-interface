# python-swfr-menu-plan-xml-interface
A simple python code accessing the XML interface of the menu plan from SWFR (Studierendenwerk Freiburg-Schwarzwald).

More informations you can find [here](https://www.swfr.de/essen/mensen-cafes-speiseplaene/speiseplan-xml-schnittstelle).

## Explanation XML interface

### API-Key

If you want to access the XML interace you need an API-Key which you can request at SWFR. The `baseurl` is:

```
https://www.swfr.de/apispeiseplan?&type=98&tx_speiseplan_pi1[apiKey]={YOUR_API_KEY}
```

### Location ID

If you want to retrieve data from a specific location you have to add following to the `baseurl`:

```
&tx_speiseplan_pi1[ort]={LOCATION_ID}
```

| Location | ID |
|:--------:|:--:|
|Mensa Rempartstraße|610|
|Mensa Institutsviertel|620|
|Mensa Littenweiler|630|
|Mensa Furtwangen|641|
|Mensa Offenburg|651|
|Mensa Gengenbach|652|
|Mensa Kehl|661|
|Mensa Schwenningen|671|
|Mensa Lörrach|677|
|Mensa Flugplatz|681|
|MusiKantine|722|
|Haus zur Lieben Hand|776|
|Otto-Hahn-Gymnasium Furtwangen|9012|

### Days

If you do not specify how many days you would like to receive the information, you will receive the information for the next 6 days (including today). If you want to limit the days displayed, you can add the following to the `url`:

```
&tx_speiseplan_pi1[tage]={DAYS}
```

|Days|Meaning|
|:--:|:-----:|
|0|today + the next 5 days|
|1|today|
|2|today + tomorrow|
|3|today + the next 2 days|
|4|today + the next 3 days|
|5|today + the next 4 days|
|6|today + the next 5 days|
|n > 6|today + the next 5 days|

Please notice:

1. Sunday is fundamentally ignored.
2. Today is always taken as the starting point. So 1 will only stand for Monday on a Monday and not always for Monday.
3. A week break is made, minus Sundays.
4. Days on which the canteen is closed are ignored. If, for example, there are public holidays and a long weekend within the next few days, fewer data records will be returned. During semester or school holidays, this can mean that no data records are returned at all.

### i18n (Internationalization)

A little fact in passing as to why we use i18n in computer science. In the English word internationalisation, there are 18 letters between the i and the n.

The interface offers the option of requesting the data in English. However, the interface only offers English or German. To access the English API, the baseurl changes as follows:

```
https://www.swfr.de/en/apispeiseplan?&type=98&tx_speiseplan_pi1[apiKey]={YOUR_API_KEY}
```

## Usage
