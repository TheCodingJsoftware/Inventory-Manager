import os

import ujson as json

from utils.workspace.flow_tag import FlowTag
from utils.workspace.flow_tags import FlowTags
from utils.workspace.status import Status
from utils.workspace.tag import Tag


class WorkspaceSettings:
    def __init__(self) -> None:
        self.filename: str = "workspace_settings"
        self.FOLDER_LOCATION: str = f"{os.getcwd()}/data"
        self.notes: str = ""
        self.tags: list[Tag] = []
        self.flow_tags_group: list[FlowTags] = []
        self.__create_file()
        self.load_data()

    def create_group(self, name: str) -> FlowTags:
        flow_tags = FlowTags(name)
        self.flow_tags_group.append(flow_tags)
        return flow_tags

    def delete_group(self, group: FlowTags):
        self.flow_tags_group.remove(group)

    def get_flow_tag_group(self, name: str) -> FlowTags:
        for group in self.flow_tags_group:
            if group.name == name:
                return group

    def add_tag(self, tag: Tag):
        self.tags.append(tag)

    def remove_tag(self, tag: Tag):
        self.tags.remove(tag)

    def get_all_tags(self) -> list[str]:
        return [tag.name for tag in self.tags]

    def get_all_statuses(self) -> list[Status]:
        statuses: list[Status] = []
        for tag in self.tags:
            statuses.extend(status.name for status in tag.statuses)
        return statuses

    def get_tag(self, tag_name: str) -> Tag:
        for tag in self.tags:
            if tag.name == tag_name:
                return tag

    def create_tag(self, name: str) -> Tag:
        tag = Tag(name, {"attribute": {}, "statuses": {}})
        self.tags.append(tag)
        return tag

    def create_flow_tag(self, flow_tags: FlowTags, name: str):
        flow_tag = FlowTag(name, [], self)
        self.add_flow_tag(flow_tags, flow_tag)

    def get_all_flow_tags(self) -> dict[str, FlowTag]:
        flow_tags: dict[str, FlowTag] = []
        for flow_tag_group in self.flow_tags_group:
            for flow_tag in flow_tag_group:
                flow_tags |= {flow_tag.get_name(): flow_tag}
        return flow_tags

    def add_flow_tag(self, flow_tags: FlowTags, flow_tag: FlowTag):
        flow_tags.add_flow_tag(flow_tag)

    def remove_flow_tag(self, flow_tags: FlowTags, flow_tag: FlowTag):
        flow_tags.remove_flow_tag(flow_tag)

    def save(self):
        with open(f"{self.FOLDER_LOCATION}/{self.filename}.json", "w", encoding="utf-8") as file:
            json.dump(self.to_dict(), file, ensure_ascii=False, indent=4)

    def __create_file(self):
        if not os.path.exists(f"{self.FOLDER_LOCATION}/{self.filename}.json"):
            self._reset_file()

    def _reset_file(self):
        with open(f"{self.FOLDER_LOCATION}/{self.filename}.json", "w", encoding="utf-8") as file:
            file.write("{}")

    def load_data(self):
        try:
            with open(f"{self.FOLDER_LOCATION}/{self.filename}.json", "r", encoding="utf-8") as file:
                data: dict[str, dict[str, object]] = json.load(file)
        except KeyError:  # Inventory was just created
            return
        except json.JSONDecodeError:  # Inventory file got cleared
            self._reset_file()

        self.notes = data.get(
            "notes",
            """Create and edit flow tags, set attributes and statuses.

If a tag box is left as 'None' it will not be part of the flow.
"Starts Timer" starts the timer if the flow tag has a timer enabled, timers will be stop automatically when flow tag is changed.
Tags such as, "Staging", "Editing", and "Planning" cannot be used as flow tags, nothing will be checked if you use them, it could break everything, so, don't use them.""",
        )
        self.tags.clear()
        self.flow_tags_group.clear()

        for tag, tag_data in data.get("tags", {}).items():
            tag = Tag(tag, tag_data)
            self.tags.append(tag)

        for group, flow_tags in data.get("flow_tags", {}).items():
            flow_tag_group = FlowTags(group)
            self.flow_tags_group.append(flow_tag_group)
            for flow_tag_name, flow_tag_data in flow_tags.items():
                flow_tag = FlowTag(flow_tag_name, flow_tag_data, self)
                flow_tag_group.add_flow_tag(flow_tag)

    def to_dict(self) -> dict[str, dict[str, dict[str, dict]]]:
        data: dict[str, dict[str, dict[str, dict]]] = {"notes": self.notes, "tags": {}, "flow_tags": {}}
        for tag in self.tags:
            data["tags"].update({tag.name: tag.to_dict()})

        for flow_tag_group in self.flow_tags_group:
            data["flow_tags"].update({flow_tag_group.name: {}})
            for flow_tag in flow_tag_group.flow_tags:
                data["flow_tags"][flow_tag_group.name].update({flow_tag.name: flow_tag.to_dict()})

        return data
