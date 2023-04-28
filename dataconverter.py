import sqlite3
from dataclasses import dataclass, asdict
import json
import pathlib

base_path = pathlib.Path(__file__).parent.resolve()
print(base_path)
db_file = f"{base_path}/ProductionDB14.bytes"

con = sqlite3.connect(db_file)
cur = con.cursor()

IMG_FOLDER = f"{base_path}/images/"


"""
id
attribute
assets
name
order
size
parent
year
code
modified

"""
@dataclass
class Base:
    @property
    def __dict__(self):
        return asdict(self)

    @property
    def json(self):
        # return json.dumps(self.__dict__)
        return self.__dict__

@dataclass
class Asset(Base):
    base_front_1: str | None = None
    base_front_2: str | None = None
    base_front_3: str | None = None
    base_back: str | None = None
    team_logo: str | None = None
    collectionBg: str | None = None


@dataclass
class Album(Base):
    id: int
    attributes: dict
    name: str
    order: int
    year: int
    code: str
    modified: int


@dataclass
class Collection(Album):
    assets: Asset
    size: int
    parent: int


album_list = []
collection_list = []

res = cur.execute("SELECT * FROM VTCollection")
result = res.fetchall()
for each in result:
    id, attributes, assets, name, order, size, parent, year, code, modified = each
    if attributes:
        attributes = json.loads(attributes)
    if assets:
        assets = Asset(**(json.loads(assets)))
        collection_list.append(
            Collection(
                id=id,
                attributes=attributes,
                assets=assets,
                name=name,
                order=order,
                size=size,
                parent=parent,
                year=year,
                code=code,
                modified=modified,
            )
        )
    else:
        album_list.append(
            Album(
                id=id,
                attributes=attributes,
                name=name,
                order=order,
                year=year,
                code=code,
                modified=modified,
            )
        )

with open(f"{base_path}/album.json", "w") as album_file:
    # json_string = json.dumps([each.json for each in album_list])
    # album_file.write(json_string)
    json.dump([each.json for each in album_list], album_file, indent=2)


with open(f"{base_path}/collection.json", "w") as collection_file:
    #  json_string = json.dumps([each.json for each in collection_list])
    #  collection_file.write(json_string)
    json.dump([each.json for each in collection_list], collection_file, indent=2)


@dataclass
class CardAsset(Base):
    img: str
    comboTitle: str | None = None
    comboIcon: str | None = None


@dataclass
class Card(Base):
    id: int
    name: str
    ccid: int
    cid: float
    assets: CardAsset
    modified: int
    formulaID: int
    power: int
    energy: int
    rarity: int
    componentNeed: int
    componentFormulaID: int | None
    fuseReady: dict | None
    code: str
    abilityTitle: str
    albumKey: str
    collectionKey: str
    matchValue: float
    acquireType: str
    hash: str
    abilityText: str
    abilityFormatCentre: int
    abilityString: list[dict] | None # Need work on this 
    tagString: list[str] | None # Need work on this 
    comboString: list[str] | None # Need work on this 
    dyk: str
    comboName: str

    def __post_init__(self):
        self.assets = CardAsset(**(json.loads(self.assets)))
        self.fuseReady = json.loads(self.fuseReady) if self.fuseReady else self.fuseReady
        self.abilityString = json.loads(self.abilityString) if self.abilityString else self.abilityString

    @property
    def __dict__(self):
        
        result = asdict(self)
        result["assets"] = self.assets.__dict__
        return result


res = cur.execute("SELECT * FROM VTCardModel")
result = res.fetchall()

card_list = []

for each in result:
    # each[4] = CardAsset(**(json.loads(each[4])))
    card_list.append(Card(*each))
print(card_list)
with open(f"{base_path}/card.json", "w") as card_file:
    #  json_string = json.dumps([each.json for each in collection_list])
    #  collection_file.write(json_string)
    card_dict = [each.json for each in card_list]
    # json.dump([each.json for each in card_list], card_file)
    json.dump(card_dict,card_file,indent=2)