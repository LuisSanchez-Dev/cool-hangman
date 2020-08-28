# -*- coding: utf-8 -*-

# Cool Hangman script for Streamlabs Chatbot
# Copyright (C) 2020 Luis Sanchez
#
# Versions:
#   - 1.0.1 08/28/2020: Fixed not blocking repeated letters
#   - 1.0.0 08/27/2020: Release

import os
import sys
import clr
import time
import json
import codecs
import threading

# Script Information
Creator = "LuisSanchezDev"
Description = "Fun minigame known as hangman now in Streamlabs Chatbot"
ScriptName = "Cool Hangman"
Version = "1.0.1"
Website = "https://www.fiverr.com/luissanchezdev"

# Define Global Variables
PATH = os.path.dirname(os.path.realpath(__file__))
SETTINGS = {}
CONFIG_FILE = os.path.join(PATH, "config.json")
WORDS_FILE = os.path.join(PATH, "words.txt")
HANGMAN_UI_FILE = os.path.join(PATH, "ui", "hangman.txt")

global current_game
current_game = {}

# Initialize Data (Only called on load)
def Init():
  global SETTINGS, CONFIG_FILE, current_game
  try:
    with codecs.open(CONFIG_FILE, encoding="utf-8-sig", mode='r') as file:
      SETTINGS = json.load(file, encoding="utf-8-sig")
  except:
    SETTINGS = {
      "cmd_play": "!starthang",
      "p_mod": "Moderator",
      "cmd_guess": "!guess",
      "cmd_guessword": "!guessword",
      "n_guess_cd": 6,
      
      "n_play_every_seconds": 600,
      "n_letter_cost": 10,
      "n_letter_prize": 12,
      "n_word_cost": 25,
      "n_tries_per_10_letters": 10,
      
      "msg_game_started": "Hangman started: $word, guess a letter with $lettercmd ($lettercost $currency) or a word with $wordcmd ($wordcost $currency)",
      "msg_letter_found": "Letter $letter appeared $times times! $user wins $prize $currency!",
      "msg_word_guessed": "🎉🎉 $user guessed \"$word\" correctly! They get $prize $currency for the last $letters letters!",
      "msg_letter_not_in_word": "The letter $letter is not in the word :(",
      "msg_word_guessed_wrong": "$word is not the correct word :(",
      "msg_cd": "$command is on cooldown for $user, wait $remaining seconds!",

      "msg_no_permission": "You don't have permission to use this command!",
      "msg_not_enough_points": "Sorry, you don't have enough $currency :(",
      "msg_game_running": "A game is already running!",
      "msg_max_tries_reached": "Max tries reached! The word was \"$word\"",
      "msg_letter_already_guessed": "The letter $letter was already guessed!",
      "msg_no_game_running": "There is no game running at the moment!",
      "msg_usage_guess": "Usage: $command <letter>",
      "msg_usage_guessword": "Usage: $command your guess"
    }
  current_game = {
    "running": False,
    "last_run": time.time(),
    "finished": False
  }
  cleanup()

# Execute Data / Process messages
def Execute(data):
  if not data.IsChatMessage():
    return
  
  
  user = data.User
  command = data.GetParam(0)
  show_cd_message = lambda: Parent.SendStreamMessage(
    SETTINGS["msg_cd"].replace(
      "$command", command
    ).replace(
      "$user", user
    ).replace(
      "$remaining", str(Parent.GetUserCooldownDuration(ScriptName, command, user))
    )
  )
  
  if command == SETTINGS["cmd_play"]:
    if is_game_running():
      Parent.SendStreamMessage(SETTINGS["msg_game_running"])
      return
    if not Parent.HasPermission(user, SETTINGS["p_mod"], ""):
      Parent.SendStreamMessage(SETTINGS["msg_no_permission"])
      return
    start_game()
  elif command == SETTINGS["cmd_guess"]:
    if not is_game_running():
      Parent.SendStreamMessage(SETTINGS["msg_no_game_running"])
      return
    if data.GetParamCount() != 2 or len(data.GetParam(1)) != 1:
      Parent.SendStreamMessage(SETTINGS["msg_usage_guess"].replace("$command", SETTINGS["cmd_guess"]))
      return
    if Parent.IsOnUserCooldown(ScriptName, command, user):
      show_cd_message()
      return
    if not Parent.RemovePoints(user, user, SETTINGS["n_letter_cost"]):
      Parent.SendStreamMessage(SETTINGS["msg_not_enough_points"].replace("$currency", Parent.GetCurrencyName()))
      return
    user_guess_letter(user, data.GetParam(1))
    Parent.AddUserCooldown(ScriptName, command, user, SETTINGS["n_guess_cd"])
  elif command == SETTINGS["cmd_guessword"]:
    if not is_game_running():
      Parent.SendStreamMessage(SETTINGS["msg_no_game_running"])
      return
    if data.GetParamCount() < 2:
      Parent.SendStreamMessage(SETTINGS["msg_usage_guessword"].replace("$command", SETTINGS["cmd_guessword"]))
      return
    if Parent.IsOnUserCooldown(ScriptName, command, user):
      show_cd_message()
      return
    if not Parent.RemovePoints(user, user, SETTINGS["n_word_cost"]):
      Parent.SendStreamMessage(SETTINGS["msg_not_enough_points"].replace("$currency", Parent.GetCurrencyName()))
      return
    user_guess_word(user, " ".join(data.Message.split(" ")[1:]))
    Parent.AddUserCooldown(ScriptName, command, user, SETTINGS["n_guess_cd"])

# Tick method (Gets called during every iteration even when there is no incoming data)
def Tick():
  global current_game, SETTINGS
  if game_ended():
    elapsed_time = time.time() - current_game["end_time"]
    if elapsed_time > 8:
      cleanup()
    return
  if is_game_running():
    return
  elapsed_time = time.time() - current_game["last_run"]
  if elapsed_time >= SETTINGS["n_play_every_seconds"]:
    start_game()

# Reload Settings (Called when a user clicks the Save Settings button in the Chatbot UI)
def ReloadSettings(jsonData):
  Init()

def is_game_running():
  global  current_game
  return current_game["running"]

def game_ended():
  global current_game
  return current_game["finished"]

def start_game():
  global  current_game
  set_ui_frame(1)
  word = get_random_word()
  hidden_word = ""
  for c in word:
    hidden_word += c if c == " " else "_"
  current_game = {
    "word": word,
    "hidden_word": hidden_word,
    "guessed": [],
    "tries": 0,
    "running": True,
    "last_run": time.time(),
    "finished": False,
    "exit_time": time.time()
  }
  Parent.SendStreamMessage(
    SETTINGS["msg_game_started"].replace(
      "$lettercmd", SETTINGS["cmd_guess"]
    ).replace(
      "$lettercost", str(SETTINGS["n_letter_cost"])
    ).replace(
      "$wordcmd", SETTINGS["cmd_guessword"]
    ).replace(
      "$wordcost", str(SETTINGS["n_word_cost"])
    ).replace(
      "$word", get_formatted_hidden_word()
    ).replace(
      "$currency", Parent.GetCurrencyName()
    )
  )
  write_to_text_ui()

def user_guess_letter(user, letter):
  global current_game
  letter = letter.lower()
  if letter in current_game["guessed"]:
    Parent.SendStreamMessage(SETTINGS["msg_letter_already_guessed"].replace("$letter", letter))
    return
  if letter not in current_game["word"].lower():
    Parent.SendStreamMessage(SETTINGS["msg_letter_not_in_word"].replace("$letter", letter))
    retry()
    return
  current_game["guessed"].append(letter)
  times_found = 0
  new_hidden_word = ""
  for i, c in enumerate(current_game["word"]):
    if c.lower() == letter:
      times_found += 1
      new_hidden_word += current_game["word"][i]
    else:
      new_hidden_word += current_game["hidden_word"][i]
  current_game["hidden_word"] = new_hidden_word
  prize = SETTINGS["n_letter_prize"] * times_found
  Parent.AddPoints(user, user, prize)
  Parent.SendStreamMessage(
    SETTINGS["msg_letter_found"].replace(
      "$letter", letter
    ).replace(
      "$times", str(times_found)
    ).replace(
      "$user", user
    ).replace(
      "$prize", str(prize)
    ).replace(
      "$currency", Parent.GetCurrencyName()
    )
  )
  if "_" not in current_game["hidden_word"]:
    Parent.SendStreamMessage(get_formatted_hidden_word())
    end_game()
  else:
    Parent.SendStreamMessage(get_formatted_hidden_word())
  write_to_text_ui()

def user_guess_word(user, word):
  global current_game
  if word.lower() != current_game["word"].lower():
    Parent.SendStreamMessage(SETTINGS["msg_word_guessed_wrong"].replace("$word", word))
    retry()
    return
  letters_left = len([c for c in current_game["hidden_word"] if c == "_"])
  prize = SETTINGS["n_letter_prize"] * letters_left
  Parent.AddPoints(user, user, prize)
  Parent.SendStreamMessage(
    SETTINGS["msg_word_guessed"].replace(
      "$user", user
    ).replace(
      "$word", current_game["word"]
    ).replace(
      "$prize", str(prize)
    ).replace(
      "$currency", Parent.GetCurrencyName()
    ).replace(
      "$letters", str(letters_left)
    )
  )
  current_game["running"] = False
  write_to_text_ui()
  end_game()

def retry():
  global current_game
  current_game["tries"] += 1
  max_tries = len(current_game["word"].replace(" ","")) * SETTINGS["n_tries_per_10_letters"] / 10
  error_percent = (7 * current_game["tries"] / max_tries) + 1
  set_ui_frame(int(error_percent))
  if current_game["tries"] >= max_tries:
    set_ui_frame(8)
    end_game()
    Parent.SendStreamMessage(SETTINGS["msg_max_tries_reached"].replace("$word", current_game["word"]))
    
def set_ui_frame(frame):
  main_path = os.path.join(PATH, "ui", "main.png")
  frame_path = os.path.join(PATH, "ui", str(frame)+".png")
  os.popen('copy "{0}" "{1}"'.format(
    frame_path, main_path
  ))

def cleanup():
  global current_game
  current_game["last_run"] = time.time() + 2
  current_game["running"] = False
  clear_text_ui()
  set_ui_frame(0)

def end_game():
  global current_game
  current_game["hidden_word"] = current_game["word"]
  write_to_text_ui()
  current_game["end_time"] = time.time()
  current_game["finished"] = True

def get_formatted_hidden_word():
  global current_game
  output = current_game["hidden_word"].replace(" ", "-")
  return " ".join(list(output))

def write_to_text_ui():
  try:
    with open(HANGMAN_UI_FILE, "w") as file:
      file.write(get_formatted_hidden_word())
  except Exception as e:
    Parent.Log(ScriptName, "Error writing text ui file: " + str(e))

def clear_text_ui():
  try:
    with open(HANGMAN_UI_FILE, "w") as file:
      file.write("")
  except Exception as e:
    Parent.Log(ScriptName, "Error writing text ui file: " + str(e))

def get_random_word():
  global WORDS_FILE
  tried_lines = 0
  lines = list(open(WORDS_FILE))
  bad_words = []
  for line in lines:
    if "-" in line or "_" in line:
      bad_words.append(line)
  if len(bad_words) > 0:
    Parent.SendStreamMessage("Could'nt start hangman, you have words that don't meet the requirements, check the Logs for more information")
    Parent.Log(ScriptName, "Fix these words:\n" + "\n".join(bad_words))
    raise ImportError
  if len(lines) > 0:
    return lines[Parent.GetRandom(0, len(lines))].replace("\r","").replace("\n","")
  else:
    Parent.SendStreamMessage("words file is empty!")
    raise IndexError

# UI Buttons
def donate():
  os.startfile("https://streamlabs.com/luissanchezdev/tip")
def open_contact_me():
  os.startfile("https://www.fiverr.com/luissanchezdev")
def open_contact_td():
  os.startfile("https://www.fiverr.com/tecno_diana")
def open_readme():
  os.startfile("https://github.com/LuisSanchez-Dev/cool-hangman")
def open_words():
  os.startfile(WORDS_FILE)
def open_ui_folder():
  os.startfile(os.path.join(PATH, "ui"))