import datetime
import uuid
import rumps

from menubar_dataclasses import Todo, TodoStatus, todostatus_lookup

from menubar_repo import TodoRepo


class MenubarTodoApp(rumps.App):
    _APP_TITLE = "𝟭✓𝟮→"
    _ICON_PATH = '1T2G_icon_1024.png'
    _CURR_TODO_PREFIX = "☑️: "
    _PAUSED_TODO_PREFIX = "➡ "
    _MAX_TODO = 3
    _NO_TODO_TEXT = "No paused todo"

    def __init__(self, DEBUG=False):
        self.DEBUG = DEBUG
        name: str = self._APP_TITLE
        super(MenubarTodoApp, self).__init__(name, quit_button=None)
        self.repo: TodoRepo = TodoRepo(rumps.application_support("1T2G"))
        self.todos = self._load_all_todo()
        self.current_todo = self._get_current_todo()
        self._create_menu()

    def _update_paused_todo_menu_items(self):
        paused_todo = self._get_todo('paused')
        print(paused_todo)
        index = 'SeparatorMenuItem_2'

        # Remove the current TD if it is hanging around

        if self._get_paused_todo_text(self.current_todo.description) in self.menu.keys():
            del self.menu[self._get_paused_todo_text(self.current_todo.description)]

        if paused_todo:
            if self._NO_TODO_TEXT in self.menu.keys():
                del self.menu[self._NO_TODO_TEXT]

            for todo in paused_todo:
                if self._get_paused_todo_text(todo.description) not in self.menu.keys():
                    self.menu.insert_after(index,
                                           rumps.MenuItem(
                                               self._get_paused_todo_text(todo.description),
                                               callback=self._set_as_current_todo))
        else:
            self.menu.insert_after(index, rumps.MenuItem(self._NO_TODO_TEXT))

    def _create_todo_menu_item(self, todo: Todo) -> [rumps.MenuItem]:
        return [rumps.MenuItem(
            self._get_paused_todo_text(todo.description),
            callback=self._set_as_current_todo),]

    def _create_paused_todo_menu_items(self) -> list[rumps.MenuItem]:
        paused_todo = self._get_todo("paused")
        print(paused_todo)
        if paused_todo:
            return [self._create_todo_menu_item(todo)[0] for todo in paused_todo]
        return [rumps.MenuItem(self._NO_TODO_TEXT), ]

    def _create_preferences_menu_items(self) -> list[rumps.MenuItem]:
        return [
            [rumps.MenuItem("Preferences"),
            # [[rumps.MenuItem("Set Max"),
            #   [rumps.MenuItem(str(i), callback=self._set_todo_limit) for i in range(1, self._MAX_TODO + 1)],
            # ],
             [[rumps.MenuItem("Debug"),
                [rumps.MenuItem("Print Menu", callback=self._print_menu),
                rumps.MenuItem("Print Todos", callback=self._print_todos),
                ],],],
            ]
        ]

    def _create_menu(self):
        new_todo_menu_items = [
            rumps.MenuItem("New Todo", callback=self._new_todo_window, key="N"),
        ]
        current_todo_action_menu_items = [
            rumps.MenuItem("Complete Current", callback=self._complete_current_todo, key="C"),
            rumps.MenuItem("Delete Current", callback=self._delete_current_todo, key="D")
        ]
        paused_todo_menu_items = self._create_paused_todo_menu_items()
        preferences_menu_items = self._create_preferences_menu_items()
        self.menu = new_todo_menu_items + \
                    [rumps.separator] + \
                    current_todo_action_menu_items + \
                    [rumps.separator] + \
                    paused_todo_menu_items + \
                    [rumps.separator] + \
                    preferences_menu_items + \
                    [rumps.separator]

    def _print_todos(self, _):
        print(self.todos)

    def _print_menu(self, _):
        self._walk_and_print_menu(_menu=self.menu)

    def _walk_and_print_menu(self, _menu=None):
        menu = _menu
        if len(menu.items()) > 0:
            item = menu.popitem(0)
            if isinstance(item, rumps.MenuItem):
                self._walk_and_print_menu(item)
            else:
                print(item[0], item[1])
                self._walk_and_print_menu(_menu=menu)

    def _load_all_todo(self) -> [Todo]:
        return self.repo.get_all_todo() if self.repo.get_all_todo() is not None else []

    def _get_current_todo(self) -> Todo:
        todos = self._get_todo("current")
        if todos is None:
            todos = self._get_todo('paused')
            if todos is None:
                return None
        return todos[0]

    def _get_todo(self, status: str = None, description: str = None) -> list[Todo]:
        if len(self.todos) > 0:
            if status is not None:
                search_status = todostatus_lookup[status]
                status_todo = [todo for todo in self.todos if todo.current_status in search_status]
                return status_todo

            if description is not None:
                desc_todo = [todo for todo in self.todos if todo.description == description][0]
                return desc_todo

        return None

    def _new_todo_window(self, sender):
        window = rumps.Window(
            title='New Todo',
            ok="Save",
            cancel="Don't Save",
            dimensions=(200, 32))
        response = window.run()
        self._add_todo(response)

    def _pop_paused_todo(self):
        paused_todos = self._get_todo("paused")
        if paused_todos:
            self._set_current_todo(paused_todos.pop())
        else:
            self.title = self._APP_TITLE

    def _complete_current_todo(self, sender) -> None:
        print("CALLBACK: Complete Current Todo") if self.DEBUG else ...
        self.current_todo.current_status = 'completed'
        self.current_todo.completed_on = datetime.datetime.now()
        self.current_todo = None
        self._pop_paused_todo()

    def _delete_current_todo(self, sender):
        print("CALLBACK: Delete Current Todo") if self.DEBUG else ...
        self.current_todo.current_status = 'deleted'
        self.current_todo = None
        self._pop_paused_todo()

    def _add_todo(self, response: rumps.rumps.Response):
        print(f"CALLBACK: Add Todo {response.text}") if self.DEBUG else ...
        if response.text == "":
            print("Todo must contain text.")
            return

        active_todo = self._get_todo(status="active")
        if active_todo:
            if response.text in [todo.description for todo in active_todo]:
                print("Todo cannot have same description of another active todo.")
                return

            if len(active_todo) + 1 > self._MAX_TODO:
                print(f"Sorry, please keep your Todo below {self._MAX_TODO}.")
                return

        new_todo = Todo(
            uuid=uuid.uuid4(),
            description=response.text,
            current_status="current",
            created_on=datetime.datetime.now(),
            completed_on=None
        )
        self.todos.append(new_todo)
        self._set_current_todo(new_todo)

    def _set_as_current_todo(self, sender):
        todo = self._get_todo(description=self._strip_paused_todo_text(sender.title))
        self._set_current_todo(todo)

    def _strip_paused_todo_text(self, text) -> str:
        return text[2:]

    def _get_paused_todo_text(self, text: str) -> str:
        return self._PAUSED_TODO_PREFIX + text

    def _get_current_todo_text(self, text: str) -> str:
        return  self._CURR_TODO_PREFIX + text

    def _set_current_todo(self, new_todo: Todo):
        """
        This function takes in ANY todo, completely new or existing, and
        evaluates if it can and should be set as Current Todo.

        :param new_todo:
        :return: None
        """
        print("CALLBACK: Set Current Todo") if self.DEBUG else ...

        # First, toggle the current TD and the new TD
        if self.current_todo:
            self.current_todo.current_status = 'paused'
        self.current_todo = new_todo
        self.current_todo.current_status = 'current'
        self.title = self._get_current_todo_text(self.current_todo.description)

        # Second, update the paused TD list
        self._update_paused_todo_menu_items()

    def _save_all_todo(self) -> None:
        print("CALLBACK: Save all Todo") if self.DEBUG else ...
        self.repo.save_all_todo(self.todos)

    @rumps.clicked("Quit")
    def quit(self, _):
        self._save_all_todo()
        rumps.quit_application()


if __name__ == '__main__':
    rumps.debug_mode(False)
    MenubarTodoApp().run()
