
---
# *client.json* overview

```json
{
	"id": 875271995644842004,
	"status": "online", 
	"activity-preset": false,
	"activities": {
		"preset-1": { "type": "playing", "cycle-interval": 3600, "list": [  ] },
		"preset-2": { "type": "watching", "cycle-interval": 600, "list": [ "Pink Panther", "Merry Melodies" ] },
		"preset-3": { "type": "listening", "cycle-interval": false, "list": [ "Some Rock", "Phonk'n mood" ] },
		"preset-4": { "type": "playing", "cycle-interval": 3600, "list": [  ] }
	}
}
```
---

## Elements description

---

### id
> _type: int_
> 
> Id of discord client representation of bot

### status
> _type: str_
> 
> Status displayed in discord just like normal account's
> 
> Possible: `online`, `offline`, `idle`, `dnd` ( aka do not disturb )


### activities
> _type: dict_
> 
> Presets of activities containing info about activities
> 
> #### In order:
> 
> ---
> 
> * ### _type_
> 
>  Type of activities, specifies message about activity ( `Playing game...`, `Watching ...` )
> 
>  #### supported: 
>  * `playing` ( default ), 
>  * `watching`, 
>  * `listening`
>  
> ---
> 
> * ###  _cycle-interval_ 
> 
>  Cycle interval ( in seconds ) between change of activity 
>  #### supported:
>  * `false` / `0` - No interval means no cycle of activities names
>  * `fast` - random number between 1,800 and 7,200 ( 0.5 to 2h )
>  * `slow` - random number between 25,200 and 36,000 ( 7 to 10h )
>  * `int` - number of seconds between change
>  
> ---
> 
> * ### _list_ 
> 
>  List of custom activities from which one will be drawn each time ( if cycle is active )
>  #### supported:
>   * list of strings with at least one record