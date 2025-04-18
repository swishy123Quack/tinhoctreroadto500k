import curses

def main(stdscr):
    # Initialize the screen
    curses.curs_set(0)  # Hide the cursor
    stdscr.clear()  # Clear the screen
    stdscr.addstr(0, 0, "Hello, curses!")
    stdscr.refresh()

    # Wait for a key press
    stdscr.getch()  # Wait for a key press before exiting

# Wrap the main function in curses.wrapper() to handle initialization and cleanup
curses.wrapper(main)