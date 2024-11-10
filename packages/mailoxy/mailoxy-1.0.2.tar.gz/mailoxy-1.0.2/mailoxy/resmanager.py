from pathlib import Path

from mailoxy.dmr import Icon, Chara, Frame, Plate


class ResourceManager:
    def __init__(self, path: str | Path):
        self.path = path if isinstance(path, Path) else Path(path)

        if not self.path.exists():
            raise FileNotFoundError(self.path)
        self.icon_path = self.path / "icons"
        self.chara_path = self.path / "chara"
        self.frame_path = self.path / "frame"
        self.plate_path = self.path / "nameplate"
        self.map = self.path / "map"

    def get_icon(self, icon: Icon) -> Path:
        return self.icon_path / f"Icon_{str(icon.name.ID).zfill(6)}.png"

    def get_chara(self, chara: Chara) -> Path:
        return self.chara_path / f"Chara_{str(chara.name.ID).zfill(6)}.png"

    def get_frame(self, frame: Frame) -> Path:
        return self.frame_path / f"Frame_{str(frame.name.ID).zfill(6)}.png"

    def get_plate(self, plate: Plate) -> Path:
        return self.plate_path / f"Plate_{str(plate.name.ID).zfill(6)}.png"

    def get_chara_frame_base(self, chara: Chara) -> Path:
        return self.map / f"csl_frame_base_{str(chara.color.ID).zfill(6)}.png"

    def get_chara_frame(self, chara: Chara) -> Path:
        return self.map / f"csl_frame_{str(chara.color.ID).zfill(6)}.png"

    def get_chara_start(self, chara: Chara):
        return self.map / f"c_start_{str(chara.color.ID).zfill(6)}.png"
