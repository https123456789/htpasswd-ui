import os
from fasthtml.common import (
    FastHTML, serve, Title, Body, Main, Div, picolink, H1, H2, Table, Tr, Td,
    Th, Button, Form, Input, A, Article, Section
)

FILE_LOCATION = os.environ.get("FILE_LOCATION", "/.htpasswd")
app = FastHTML(hdrs=(picolink))


# Data Functions


def get_users():
    users = []

    with open(FILE_LOCATION, "r") as file:
        line = file.readline()
        while line != "":
            user = line.split(":")
            users.append(user)
            line = file.readline()

    return users


def set_users(users):
    with open(FILE_LOCATION, "w") as file:
        for user in users:
            line = ":".join(user)
            file.write(line)


# Components


def main(*inner):
    return Body(Main(*inner, cls="container"))


def index_page(error=None):
    return (
        Title("Htpasswd UI"),
        main(
            H1(A("Htpasswd UI", href="/"), style="margin-bottom: 2em"),
            Section(
                H2("Users"),
                Div(hx_get="/users", hx_trigger="load", id="users_div"),
                style="margin-bottom: 2em"
            ),
            Section(
                H2("Add User"),
                error,
                Form(
                    Input(type="text", name="username"),
                    Input(type="password", name="password"),
                    Button("Submit"),
                    action="/",
                    method="post"
                ),
                style="margin-bottom: 2em"
            )
        )
    )


# Routes


@app.get("/")
def rt_root():
    return index_page()


@app.get("/users")
def rt_users():
    users = get_users()

    return Table(
        Tr(
            Th("Username"),
            Th("Actions")
        ),
        *[
            Tr(
                Td(username),
                Td(Button(
                    "Delete",
                    hx_post=f"/delete/{i}",
                    hx_target="#users_div",
                    hx_swap="innerHTML"
                ))
            )

            for i, (username, _) in enumerate(users)
        ]
    )


@app.post("/delete/{index}")
def rt_delete(index: int):
    users = get_users()

    if index >= len(users):
        return None

    users.pop(index)
    set_users(users)

    return Div(
        hx_get="/users",
        hx_trigger="load",
        hx_target="#users_div",
        hx_swap="innerHTML"
    )


@app.post("/")
def rt_add_user(username: str, password: str):
    status = os.system(f"htpasswd -bB {FILE_LOCATION} {username} {password}")

    print(status)
    if status != 0:
        return index_page(Article(
            "Failed to set password",
            style="background-color: #b71c1c33; border: 1px solid red"
        ))

    return index_page()


serve()
