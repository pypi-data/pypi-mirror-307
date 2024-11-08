import os
import shutil
import tempfile
import time
from pathlib import Path

os.environ["TZ"] = "UTC"

time.tzset()

expected_md = """[2022-08-10 19:33:38] Me: Test message  

[2022-08-10 19:33:48] Me: Test image  ![2022-08-10T19-33-48.638_00_signal-2022-08-10-153348.jpeg](./media/2022-08-10T19-33-48.638_00_signal-2022-08-10-153348.jpeg)  

[2022-08-10 19:34:11] Me:   [2022-08-10T19-34-11.986_00_Voice_Message_10-08-2022_15-34.m4a](./media/2022-08-10T19-34-11.986_00_Voice_Message_10-08-2022_15-34.m4a)  

"""  # noqa

expected_html = """<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8"/>
        <title>
            Test
        </title>
        <link href="../style.css" rel="stylesheet"/>
    </head>
    <body>
        <div class="first">
            <a href="#pg0">
                FIRST
            </a>
        </div>
        <div class="last">
            <a href="#pg0">
                LAST
            </a>
        </div>
        <div class="page" id="pg0">
            <nav>
                <div class="prev">
                    PREV
                </div>
                <div class="next">
                    NEXT
                </div>
            </nav>
            <div class="msg me">
                <span class="date">
                    2022-08-10
                </span>
                <span class="time">
                    19:33:38
                </span>
                <span class="sender">
                    Me
                </span>
                <span class="body">
                    <p>
                        Test message
                    </p>
                </span>
                <span class="reaction">
                </span>
            </div>
            <div class="msg me">
                <span class="date">
                    2022-08-10
                </span>
                <span class="time">
                    19:33:48
                </span>
                <span class="sender">
                    Me
                </span>
                <span class="body">
                    <p>
                        Test image
                    </p>
                    <figure>
                        <label for="2022-08-10T19-33-48.638_00_signal-2022-08-10-153348.jpeg">
                            <img alt="2022-08-10T19-33-48.638_00_signal-2022-08-10-153348.jpeg" load="lazy" src="./media/2022-08-10T19-33-48.638_00_signal-2022-08-10-153348.jpeg"/>
                        </label>
                        <input class="modal-state" id="2022-08-10T19-33-48.638_00_signal-2022-08-10-153348.jpeg" type="checkbox"/>
                        <div class="modal">
                            <label for="2022-08-10T19-33-48.638_00_signal-2022-08-10-153348.jpeg">
                                <div class="modal-content">
                                    <img alt="2022-08-10T19-33-48.638_00_signal-2022-08-10-153348.jpeg" class="modal-photo" loading="lazy" src="./media/2022-08-10T19-33-48.638_00_signal-2022-08-10-153348.jpeg"/>
                                </div>
                            </label>
                        </div>
                    </figure>
                </span>
                <span class="reaction">
                </span>
            </div>
            <div class="msg me">
                <span class="date">
                    2022-08-10
                </span>
                <span class="time">
                    19:34:11
                </span>
                <span class="sender">
                    Me
                </span>
                <span class="body">
                    <audio controls="">
                        <source src="./media/2022-08-10T19-34-11.986_00_Voice_Message_10-08-2022_15-34.m4a" type="audio/mp4"/>
                    </audio>
                </span>
                <span class="reaction">
                </span>
            </div>
            <script>
                if (!document.location.hash) document.location.hash = 'pg0'
            </script>
        </div>
    </body>
</html>

"""  # noqa


def test_integration():
    from sigexport.main import main

    root = Path(__file__).resolve().parents[0]
    dest = Path(tempfile.TemporaryDirectory().name)
    source = root / "data"

    main(
        None,  # type: ignore
        dest=dest,
        source=source,
        old=None,
        paginate=100,
        chats="",
        list_chats=False,
        include_empty=False,
        verbose=True,
    )

    output_test = dest / "Test"
    output_media = output_test / "media"
    output_md = (output_test / "chat.md").read_text()
    output_html = (output_test / "index.html").read_text()

    print()
    print()
    print(output_md)
    print()
    print()

    assert expected_md == output_md
    assert expected_html == output_html

    assert (
        output_media / "2022-08-10T19-33-48.638_00_signal-2022-08-10-153348.jpeg"
    ).is_file()
    assert (
        output_media / "2022-08-10T19-34-11.986_00_Voice_Message_10-08-2022_15-34.m4a"
    ).is_file()

    shutil.rmtree(dest)
