# iMessage Parser

This python script takes the iMessage Database provided by its path and prints out the conversations with another (hopefully) human being. The output will be generated as Markdown.

## Outline

I recently was asked how I would tackle this problem and got hooked right away, since it's the first little tool I wrote for myself in Python. It's quite useful: Have you ever wondered, what messages of significance you exchanged with a loved one? You are not fluid in the binary language that is in SQLite3 Database files and don't like the messages to be tucked into the iMessages App that is so cumbersome to print on paper? Take this script and export your messages into Markdown to make them easily manageable!

## Requirements

`imessage_parser.py` requires Python 3+ and the `sqlite3` library (among others, which are installed with Python by default).

## Usage

`imessage_parser.py` takes its settings inside the file itself. The following variables are given to be modified to your needs:

```python
my_name         = "Jan"
dbpath          = "~/Library/Messages/chat.db"
opponent        = ["imessage@example.com", "+49160123456789"]
opponent_name   = "Opponent"
output_file     = "conversation.md"
```

* `my_name`: This is obviously mine (i.e. in your case: your) name. This will be inserted into the exported document
* `dbpath`: Enter the path to the message database of iMessage. Normally, `~/Library/Messages/chat.db` is already correct for the regular Mac user.
* `opponent`: Here you have to enter the email address and/or phone number the opponent in question uses iMessage with. As this is a list, multiple "accounts" may be defined, for example, if the user tends to switch between iPhone and Mac. All messages will be properly interleaved in a chronicle manner.
`opponent_name`: Just a more pleasant title for the opponent, will be inserted into the exported document.
`output_file`: Provide any filename you want the conversation export to be saved to.

## Format

Just as an example, here's an example of the formated output inside of the conversational Markdown file. The attentive audience will notice, that some timestamps include multiple lines instead of just one. This is where the timestamps of consecutive messages have been combined into one, so the conversation is not cluttered by formalia.

```markdown
## 10.10.2013

**Jan [09:05:09]**
> Lorem ipsum dolor sit amet, consetetur sadipscing elitr.

**Opponent [09:04:00]**
> At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.

**Jan [09:09:25]**
> Sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.
>
> At vero eos et accusam et justo duo dolores et ea rebum.

## 07.11.2013

**Opponent [11:58:56]**
> Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at vero eros et accumsan et iusto odio dignissim qui blandit praesent luptatum zzril delenit augue duis dolore te feugait nulla facilisi.

**Jan [11:59:50]**
> Ut wisi enim ad minim veniam, quis nostrud exerci tation ullamcorper suscipit lobortis nisl ut aliquip ex ea commodo consequat.
```

## Todo

* Add support for direct HTML export
* Maybe transfer the settings to command line options?
* Streamline database queries and code

## License

Copyright (c) 2014 Jan Willhaus

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
