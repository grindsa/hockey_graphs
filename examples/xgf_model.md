# expected goal model
## model description

### "shots" subtree

separated by "home" and "visitor"

per "x"/"y" coordinate containing:
- side (left/right) - ('side')
- amount of shots, goals from this position - ('shots, 'goals')
- amount of shots and goals by "left hand" players from this position - ('lhp_shots', 'lhp_goals')
- amount of shots and goals by "right hand" players from this position - ('rhp_shots', 'rh_goals')
- amount of shots and goals from this position due to a rebound - ('rb_shots', 'rb_goals')
- amount of shots and goals from this position due to a break - ('br_shots', 'br_goals')
- calculated percentage values for the above ('shots_pctg', 'lh_pctg', 'rh_pctg', 'rb_pctg', 'br_pctg')

```json
"shots": {
    "home": {
        "59": {
            "-21": {
                "side": "right",
                "shots": 4,
                "goals": 0,
                "lhp_shots": 4,
                "lhp_goals": 0,
                "rhp_shots": 0,
                "rh_goals": 0,
                "rb_shots": 0,
                "rb_goals": 0,
                "br_shots": 0,
                "br_goals": 0,
                "shots_pctg": 0.0,
                "lh_pctg": 0.0,
                "rh_pctg": 0,
                "rb_pctg": 0,
                "rb_pctg": 0
            },
            "-28": {
                "side": "right",
                "shots": 6,
                "goals": 0,
                "lhp_shots": 3,
                "lhp_goals": 0,
                "rhp_shots": 3,
                "rh_goals": 0,
                "rb_shots": 0,
                "rb_goals": 0,
                "br_shots": 0,
                "br_goals": 0,
                "shots_pctg": 0.0,
                "lh_pctg": 0.0,
                "rh_pctg": 0.0,
                "rb_pctg": 0,
                "rb_pctg": 0
            }
        }
    }
}
```

### "handness" subtree

separated by "home" and "visitor"
per "y" coordinate, further split by "left and "right" hand  containing:
- amount of shots and goals - ('shots, 'goals')
- shot-percentage - ('shots_pctg')

```json
"handness": {
    "home": {
        "-21": {
            "side": "right",
            "left": {
                "shots": 209,
                "goals": 14,
                "shots_pctg": 6.7
            },
            "right": {
                "shots": 130,
                "goals": 5,
                "shots_pctg": 3.8
            }
        },
        "24": {
            "side": "left",
            "left": {
                "shots": 180,
                "goals": 15,
                "shots_pctg": 8.3
            },
            "right": {
                "shots": 84,
                "goals": 6,
                "shots_pctg": 7.1
            }
        },
    "visitor": {
        "-40": {
            "side": "left",
            "left": {
                "shots": 162,
                "goals": 1,
                "shots_pctg": 0.6
            },
            "right": {
                "shots": 67,
                "goals": 5,
                "shots_pctg": 7.5
            }
        },
        "19": {
            "side": "right",
            "left": {
                "shots": 157,
                "goals": 9,
                "shots_pctg": 5.7
            },
            "right": {
                "shots": 94,
                "goals": 8,
                "shots_pctg": 8.5
            }
        }        
      }
   }
}
```
### "rebounds" subtree

per "second" of rebound interval:
- amount of shots and goals - ('shots, 'goals')
- shot-percentage - ('shots_pctg')

```json
"rebounds": {
    "3": {
        "shots": 753,
        "goals": 76,
        "shots_pctg": 10.1
    },
    "0": {
        "shots": 1040,
        "goals": 274,
        "shots_pctg": 26.3
    },
}
```

### "breaks" subtree

per "second" of break interval:
- amount of shots and goals - ('shots, 'goals')
- shot-percentage - ('shots_pctg')

```json
"breaks": {
    "1": {
        "shots": 27,
        "goals": 2,
        "shots_pctg": 7.4
    },
    "2": {
        "shots": 32,
        "goals": 6,
        "shots_pctg": 18.8
    },
}
```    
