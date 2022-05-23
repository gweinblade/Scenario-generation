import json
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


"""
format of tree is
dict {
    tree_id: tree_id_text
    context: context text?
    first_story_block
    action_results: [act_res1, act_res2, act_res3...]
}

where each action_result's format is:
dict{
    action: action_text
    result: result_text
    action_results: [act_res1, act_res2, act_res3...]
}
"""


class Scraper:
    def __init__(self):
        chrome_options = Options()
        #chrome_options.add_argument("--binary=C:\Program Files (x86)\chromedriver.exe")
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--window-size=1920x1080")
        exec_path = "C:\Program Files (x86)\chromedriver.exe"
        self.driver = webdriver.Chrome(
             ChromeDriverManager().install()
        )
        self.max_depth = 10
        self.end_actions = {
            "End Game and Leave Comments",
            "Click here to End the Game and Leave Comments",
            "See How Well You Did (you can still back-page afterwards if you like)",
            "You have died.",
            "You have died",
            "Epilogue",
            "Save Game",
            "Your quest might have been more successful...",
            "5 - not the best, certainly not the worst",
            "The End! (leave comments on game)",
            "The End",
            "Truth mode.",
            "Truth Mode",
            "Bad End 1",
            "Bad End 2",
            "Bad End 3; Erased from existance",
            "Bad End 4; Death By Ignorance",
            "Bad End 5; No Time Left",
            "Bad End 6; Burned Alive",
            "Bad End 7; Sphinx attack",
            "To be Continued. . . End Game and Leave Comments",
            "Good End 2; Business As Usual",
            "Good End 3; A friend in me",
            "Start Over",
            "6 - it's worth every cent",
            "You do not survive the journey to California",
            "Quit the game.",
            "7 - even better than Reeses' Cups®",
            "8 - it will bring you enlightenment",
            "End of game! Leave a comment!",
            "Better luck next time",
            "click here to continue",
            "Rating And Leaving Comments",
            "You do not survive your journey to California",
            "Your Outlaw Career has come to an end",
            "Thank you for taking the time to read my story",
            "You have no further part in the story, End Game and Leave Comments",
            "",
            "I'm gonna sing the death song: Death, death, death, death...",
            "Face her Riddles",
            "You play no further part in this story. End Game and Leave Comments",
            "drivers",
            "Eaten by sharks",
            "That's unfortunate",
            "Dead!",
            "GOOD JOB YOU WIN!",
            "Aw, nuts!!",
            "You're so dead",
            "Pain sucks!",
            "Eaten by the serpent",
            "My heart bleeds for you",
            "Too bad...",
            "Death is such a nasty word.",
            "Too bad",
            "Blub, blub...",
            "You're going to die, now",
            "You should be ashamed of yourself",
            "Your adventure begins... all over again!",
            "Decapitated!",
            "Sharks can be murder",
            "Alas, poor Yorick, they slew you well",
            "My heart bleeds for you",
            "To End the Game and Leave Comments click here",
            "Call it a day",
            "Check the voicemail.",
            "reset",
            "There's nothing you can do anymore...it's over.",
            "To Be Continued...",
            "Thanks again for taking the time to read this",
            "If you just want to escape this endless story you can do that by clicking here",
            "Boo Hoo Hoo",
            "End.",
            "Pick up some money real quick",
            "",
            "Good End",
            "Synopsis mode. (Was there something you wanted to know? Click here!) *Spoiler Alert!*",
            "Well you did live a decent amount of time in the Army",
            "End Game",
            "You have survived the Donner Party's journey to California!",
            "Thank you for playing my game, leave a comment to see your Score!",
        }
        self.texts = set()

    def GoToURL(self, url):
        self.texts = set()
        self.driver.get(url)
        time.sleep(0.5)

    def GetText(self):
        div_elements = self.driver.find_elements_by_css_selector("div")
        text = div_elements[3].text
        return text

    def GetLinks(self):
        return self.driver.find_elements_by_css_selector("a")

    def GoBack(self):
        self.GetLinks()[0].click()
        time.sleep(0.2)

    def ClickAction(self, links, action_num):
        links[action_num + 4].click()
        time.sleep(0.2)

    def GetActions(self):
        return [link.text for link in self.GetLinks()[4:]]

    def NumActions(self):
        return len(self.GetLinks()) - 4

    def BuildTreeHelper(self, parent_story, action_num, depth, old_actions):
        depth += 1
        action_result = {}

        action = old_actions[action_num]
        print("Action is ", repr(action))
        action_result["action"] = action

        links = self.GetLinks()
        if action_num + 4 >= len(links):
            return None

        self.ClickAction(links, action_num)
        result = self.GetText()
        if result == parent_story or result in self.texts:
            self.GoBack()
            return None

        self.texts.add(result)
        print(len(self.texts))

        action_result["result"] = result

        actions = self.GetActions()
        action_result["action_results"] = []

        for i, action in enumerate(actions):
            if actions[i] not in self.end_actions:
                sub_action_result = self.BuildTreeHelper(result, i, depth, actions)
                if action_result is not None:
                    action_result["action_results"].append(sub_action_result)

        self.GoBack()
        return action_result

    def BuildStoryTree(self, url):
        scraper.GoToURL(url)
        text = scraper.GetText()
        actions = self.GetActions()
        story_dict = {}
        story_dict["tree_id"] = url
        story_dict["context"] = ""
        story_dict["first_story_block"] = text
        story_dict["action_results"] = []

        for i, action in enumerate(actions):
            if action not in self.end_actions:
                action_result = self.BuildTreeHelper(text, i, 0, actions)
                if action_result is not None:
                    story_dict["action_results"].append(action_result)
            else:
                print("done")

        return story_dict


def save_tree(tree, filename):
    with open(filename, "w") as fp:
        json.dump(tree, fp)
scraper = Scraper()
urls = [

   "https://chooseyourstory.com/story/viewer/default.aspx?StoryId=106",
   "https://chooseyourstory.com/story/viewer/default.aspx?StoryId=36462",
   "https://chooseyourstory.com/story/viewer/default.aspx?StoryId=38525",
   "https://chooseyourstory.com/story/viewer/default.aspx?StoryId=25611",
   "https://chooseyourstory.com/story/viewer/default.aspx?StoryId=60875",
   "https://chooseyourstory.com/story/viewer/default.aspx?StoryId=62020"
   
   


]

for i in range(len(urls)):
    print("****** Extracting Adventure ", urls[i], " ***********")
    tree = scraper.BuildStoryTree(urls[i])
    save_tree(tree, "stories/story" + str(36 + i) + ".json")

print("done")
