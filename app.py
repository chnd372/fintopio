from colorama import *
from datetime import datetime, timedelta
from fake_useragent import FakeUserAgent
from time import sleep
import requests
import json
import os
import random
import sys

class Fintopio:
    def __init__(self) -> None:
        self.session = requests.Session()
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'Cache-Control': 'no-cache',
            'Host': 'fintopio-tg.fintopio.com',
            'Origin': 'https://fintopio-tg.fintopio.com',
            'Pragma': 'no-cache',
            'Priority': 'u=3, i',
            'Referer': 'https://fintopio-tg.fintopio.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': FakeUserAgent().random,
            'webapp': 'true'
        }

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_timestamp(self, message):
        print(
            f"{Fore.BLUE + Style.BRIGHT}[ {datetime.now().astimezone().strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
            f"{message}",
            flush=True
        )

    def activate_referrals(self, token: str):
        url = 'https://fintopio-tg.fintopio.com/api/referrals/activate'
        data = json.dumps({'code':'l5bYPIC8FtjMColV'})
        self.headers.update({'Authorization': f'Bearer {token}'})
        try:
            response = self.session.post(url=url, headers=self.headers, data=data)
            response.raise_for_status()
            return True
        except (Exception, requests.HTTPError, requests.RequestException):
            return False

    def daily_checkins(self, token: str):
        url = 'https://fintopio-tg.fintopio.com/api/daily-checkins'
        self.headers.update({'Authorization': f'Bearer {token}'})
        try:
            response = self.session.post(url=url, headers=self.headers)
            response.raise_for_status()
            daily_checkins = response.json()
            if daily_checkins is not None:
                if daily_checkins['claimed']:
                    self.print_timestamp(f"{Fore.MAGENTA + Style.BRIGHT}[ Daily Checkins Already Claimed ]{Style.RESET_ALL}")
                else:
                    self.print_timestamp(
                        f"{Fore.GREEN + Style.BRIGHT}[ Daily Checkins Claimed ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.BLUE + Style.BRIGHT}[ Reward {daily_checkins['dailyReward']} ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT}[ Day {daily_checkins['totalDays']} ]{Style.RESET_ALL}"
                    )
            else:
                self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ There Is No Data In Daily Checkins ]{Style.RESET_ALL}")
        except requests.HTTPError as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Daily Checkins: {str(e)} ]{Style.RESET_ALL}")
        except requests.RequestException as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ A Request Error Occurred While Daily Checkins: {str(e)} ]{Style.RESET_ALL}")
        except Exception as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Daily Checkins: {str(e)} ]{Style.RESET_ALL}")

    def state_farming(self, token: str):
        url = 'https://fintopio-tg.fintopio.com/api/farming/state'
        self.headers.update({'Authorization': f'Bearer {token}'})
        try:
            response = self.session.get(url=url, headers=self.headers)
            response.raise_for_status()
            state_farming = response.json()
            if state_farming is not None:
                return state_farming
            else:
                self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ There Is No Data In State Farming ]{Style.RESET_ALL}")
        except requests.HTTPError as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Fetching State Farming: {str(e)} ]{Style.RESET_ALL}")
        except requests.RequestException as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ A Request Error Occurred While Fetching State Farming: {str(e)} ]{Style.RESET_ALL}")
        except Exception as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Fetching State Farming: {str(e)} ]{Style.RESET_ALL}")

    def farm_farming(self, token: str):
        url = 'https://fintopio-tg.fintopio.com/api/farming/farm'
        self.headers.update({'Authorization': f'Bearer {token}'})
        try:
            response = self.session.post(url=url, headers=self.headers)
            response.raise_for_status()
            farm_farming = response.json()
            if farm_farming is not None:
                if farm_farming['state'] == 'farmed':
                    self.claim_farming(token=token)
                elif farm_farming['state'] == 'farming':
                    now = datetime.now().astimezone()
                    finish = datetime.fromtimestamp(farm_farming['timings']['finish'] / 1000).astimezone()
                    self.print_timestamp(f"{Fore.GREEN + Style.BRIGHT}[ Farming Started ]{Style.RESET_ALL}")
                    if now >= finish:
                        self.claim_farming(token=token)
                    else:
                        formatted_finish = finish.strftime('%x %X %Z')
                        self.print_timestamp(f"{Fore.YELLOW + Style.BRIGHT}[ Farming Can Be Claim At {formatted_finish} ]{Style.RESET_ALL}")
                else:
                    self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ I Can Not Do Anything When 'state' In Farm Farming Is {farm_farming['state']} ]{Style.RESET_ALL}")
            else:
                self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ There Is No Data In Farm Farming ]{Style.RESET_ALL}")
        except requests.HTTPError as e:
            error_farm_farming = e.response.json()
            if e.response.status_code == 400 and error_farm_farming['message'] == 'Farming has been already started':
                self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ Farming Has Been Already Started ]{Style.RESET_ALL}")
            else:
                self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Farm Farming: {str(e)} ]{Style.RESET_ALL}")
        except requests.RequestException as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ A Request Error Occurred While Farm Farming: {str(e)} ]{Style.RESET_ALL}")
        except Exception as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Farm Farming: {str(e)} ]{Style.RESET_ALL}")

    def claim_farming(self, token: str, farmed: int):
        url = 'https://fintopio-tg.fintopio.com/api/farming/claim'
        self.headers.update({'Authorization': f'Bearer {token}'})
        try:
            response = self.session.post(url=url, headers=self.headers)
            response.raise_for_status()
            claim_farming = response.json()
            if claim_farming is not None:
                if claim_farming['state'] == 'idling':
                    self.print_timestamp(f"{Fore.GREEN + Style.BRIGHT}[ Farming Claimed {farmed} ]{Style.RESET_ALL}")
                    self.farm_farming(token=token)
                elif claim_farming['state'] == 'farming':
                    now = datetime.now().astimezone()
                    finish = datetime.fromtimestamp(claim_farming['timings']['finish'] / 1000).astimezone()
                    if now >= finish:
                        self.claim_farming(token=token)
                    else:
                        self.print_timestamp(f"{Fore.MAGENTA + Style.BRIGHT}[ Farming {claim_farming['farmed']} / {claim_farming['settings']['reward']} ]{Style.RESET_ALL}")
                        formatted_finish = finish.strftime('%x %X %Z')
                        self.print_timestamp(f"{Fore.YELLOW + Style.BRIGHT}[ Farming Can Be Claim At {formatted_finish} ]{Style.RESET_ALL}")
                else:
                    self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ There Is No 'state' In Claim Farming ]{Style.RESET_ALL}")
            else:
                self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ There Is No Data In Claim Farming ]{Style.RESET_ALL}")
        except requests.HTTPError as e:
            error_claim_farming = e.response.json()
            if e.response.status_code == 400 and error_claim_farming['message'] == 'Farming is not finished yet':
                self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ Farming Is Not Finished Yet ]{Style.RESET_ALL}")
            else:
                self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Claim Farming: {str(e)} ]{Style.RESET_ALL}")
        except requests.RequestException as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ A Request Error Occurred While Claim Farming: {str(e)} ]{Style.RESET_ALL}")
        except Exception as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Claim Farming: {str(e)} ]{Style.RESET_ALL}")

    def state_diamond(self, token: str):
        url = 'https://fintopio-tg.fintopio.com/api/clicker/diamond/state'
        self.headers.update({'Authorization': f'Bearer {token}'})
        try:
            response = self.session.get(url=url, headers=self.headers)
            response.raise_for_status()
            state_diamond = response.json()
            if state_diamond is not None:
                return state_diamond
            else:
                self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ There Is No Data In State Diamond ]{Style.RESET_ALL}")
        except requests.HTTPError as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Fetching State Diamond: {str(e)} ]{Style.RESET_ALL}")
        except requests.RequestException as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ A Request Error Occurred While Fetching State Diamond: {str(e)} ]{Style.RESET_ALL}")
        except Exception as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Fetching State Diamond: {str(e)} ]{Style.RESET_ALL}")

    def complete_diamond(self, token: str, diamond_number: str, total_reward: str):
        url = 'https://fintopio-tg.fintopio.com/api/clicker/diamond/complete'
        data = json.dumps({'diamondNumber':diamond_number})
        self.headers.update({
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        })
        try:
            response = self.session.post(url=url, headers=self.headers, data=data)
            response.raise_for_status()
            self.print_timestamp(f"{Fore.GREEN + Style.BRIGHT}[ Claimed {total_reward} From State Diamond ]{Style.RESET_ALL}")
        except requests.HTTPError as e:
            error_complete_diamond = e.response.json()
            if e.response.status_code == 400 and error_complete_diamond['message'] == 'Game is not available at the moment':
                self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ Game Is Not Available At The Moment ]{Style.RESET_ALL}")
            elif e.response.status_code == 400 and error_complete_diamond['message'] == 'The diamond is outdated, reload the page and try again':
                self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ The Diamond Is Outdated, Reload The Page And Try Again ]{Style.RESET_ALL}")
            elif e.response.status_code == 400 and error_complete_diamond['message'] == 'Game is already finished, please wait until the next one is available':
                self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ The Diamond Is Outdated, Reload The Page And Try Again ]{Style.RESET_ALL}")
            elif e.response.status_code == 400 and error_complete_diamond['message']['diamondNumber']['isNumberString'] == 'diamondNumber must be a number string':
                self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ Diamond Number Must Be A Number String ]{Style.RESET_ALL}")
            else:
                self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Complete Diamond: {str(e)} ]{Style.RESET_ALL}")
        except requests.RequestException as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ A Request Error Occurred While Complete Diamond: {str(e)} ]{Style.RESET_ALL}")
        except Exception as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Complete Diamond: {str(e)} ]{Style.RESET_ALL}")

    def tasks(self, token: str):
        url = 'https://fintopio-tg.fintopio.com/api/hold/tasks'
        self.headers.update({'Authorization': f'Bearer {token}'})
        try:
            response = self.session.get(url=url, headers=self.headers)
            response.raise_for_status()
            tasks = response.json().get('tasks', [])
            for task in tasks:
                if task['status'] == 'available':
                    self.print_timestamp(f"{Fore.YELLOW + Style.BRIGHT}[ Starting {task['slug']} ]{Style.RESET_ALL}")
                    self.start_tasks(token=token, task_id=task['id'], task_slug=task['slug'], task_reward_amount=task['rewardAmount'])
                elif task['status'] == 'verified':
                    self.print_timestamp(f"{Fore.YELLOW + Style.BRIGHT}[ Claiming {task['slug']} ]{Style.RESET_ALL}")
                    self.claim_tasks(token=token, task_id=task['id'], task_slug=task['slug'], task_reward_amount=task['rewardAmount'])
        except requests.HTTPError as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Fetching Tasks: {str(e)} ]{Style.RESET_ALL}")
        except requests.RequestException as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ A Request Error Occurred While Fetching Tasks: {str(e)} ]{Style.RESET_ALL}")
        except Exception as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Fetching Tasks: {str(e)} ]{Style.RESET_ALL}")

    def start_tasks(self, token: str, task_id: int, task_slug: str, task_reward_amount: int):
        url = f'https://fintopio-tg.fintopio.com/api/hold/tasks/{task_id}/start'
        self.headers.update({'Authorization': f'Bearer {token}'})
        try:
            response = self.session.post(url=url, headers=self.headers)
            response.raise_for_status()
            start_tasks = response.json()
            if start_tasks is not None:
                if start_tasks['status'] == 'verifying':
                    sleep(random.choice([10, 20]))
                    self.claim_tasks(token=token, task_id=task_id, task_slug=task_slug, task_reward_amount=task_reward_amount)
                elif start_tasks['status'] == 'in-progress':
                    self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ Finish This {task_slug} By Itself ]{Style.RESET_ALL}")
            else:
                self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ There Is No Data In Start Tasks ]{Style.RESET_ALL}")
        except requests.HTTPError as e:
            error_start_tasks = e.response.json()
            if e.response.status_code == 400 and error_start_tasks['message'] == 'Unable to update task status':
                self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ Unable To Update Task Status. Please Try This Task By Itself ]{Style.RESET_ALL}")
            else:
                self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Start Tasks: {str(e)} ]{Style.RESET_ALL}")
        except requests.RequestException as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ A Request Error Occurred While Start Tasks: {str(e)} ]{Style.RESET_ALL}")
        except Exception as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Start Tasks: {str(e)} ]{Style.RESET_ALL}")

    def claim_tasks(self, token: str, task_id: int, task_slug: str, task_reward_amount: int):
        url = f'https://fintopio-tg.fintopio.com/api/hold/tasks/{task_id}/claim'
        self.headers.update({'Authorization': f'Bearer {token}'})
        while True:
            try:
                response = self.session.post(url=url, headers=self.headers)
                response.raise_for_status()
                claim_tasks = response.json()
                if claim_tasks is not None:
                    if claim_tasks['status'] == 'completed':
                        self.print_timestamp(
                            f"{Fore.GREEN + Style.BRIGHT}[ Claimed {task_slug} ]{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                            f"{Fore.BLUE + Style.BRIGHT}[ Reward {task_reward_amount} ]{Style.RESET_ALL}"
                        )
                    break
                else:
                    self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ There Is No Data In Start Tasks ]{Style.RESET_ALL}")
                    break
            except requests.HTTPError as e:
                error_claim_tasks = e.response.json()
                if e.response.status_code == 400 and error_claim_tasks['message'] == 'Entity not found':
                    self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ {task_slug} Not Found ]{Style.RESET_ALL}")
                    break
                elif e.response.status_code == 400 and error_claim_tasks['message'] == 'Unable to update task status':
                    self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ Please Wait Until {task_slug} Is Claimed ]{Style.RESET_ALL}")
                    sleep(random.choice([5, 10]))
                else:
                    self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Claim Tasks: {str(e)} ]{Style.RESET_ALL}")
                    break
            except requests.RequestException as e:
                self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ A Request Error Occurred While Claim Tasks: {str(e)} ]{Style.RESET_ALL}")
                break
            except Exception as e:
                self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Claim Tasks: {str(e)} ]{Style.RESET_ALL}")
                break

    def main(self):
        while True:
            try:
                tokens = [line.strip() for line in open('tokens.txt') if line.strip()]
                farming_times = []
                for index, token in enumerate(tokens):
                    self.print_timestamp(f"{Fore.CYAN + Style.BRIGHT}[ {index + 1} ]{Style.RESET_ALL}")
                    self.activate_referrals(token=token)
                    self.daily_checkins(token=token)
                self.print_timestamp(f"{Fore.WHITE + Style.BRIGHT}[ Farming ]{Style.RESET_ALL}")
                for index, token in enumerate(tokens):
                    self.print_timestamp(f"{Fore.CYAN + Style.BRIGHT}[ {index + 1} ]{Style.RESET_ALL}")
                    state_farming = self.state_farming(token=token)
                    if state_farming['state'] == 'farmed':
                        self.claim_farming(token=token, farmed=state_farming['farmed'])
                    elif state_farming['state'] == 'idling':
                        self.farm_farming(token=token)
                    elif state_farming['state'] == 'farming':
                        now = datetime.now().astimezone()
                        finish = datetime.fromtimestamp(state_farming['timings']['finish'] / 1000).astimezone()
                        farming_times.append(finish.timestamp())
                        if now >= finish:
                            self.claim_farming(token=token, farmed=state_farming['farmed'])
                        else:
                            self.print_timestamp(f"{Fore.MAGENTA + Style.BRIGHT}[ Farming {state_farming['farmed']} / {state_farming['settings']['reward']} ]{Style.RESET_ALL}")
                            formatted_finish = finish.strftime('%x %X %Z')
                            self.print_timestamp(f"{Fore.YELLOW + Style.BRIGHT}[ Farming Can Be Claim At {formatted_finish} ]{Style.RESET_ALL}")
                    else:
                        self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ I Can Not Do Anything When 'state' In State Farming Is {state_farming['state']} ]{Style.RESET_ALL}")
                self.print_timestamp(f"{Fore.WHITE + Style.BRIGHT}[ Tasks ]{Style.RESET_ALL}")
                for index, token in enumerate(tokens):
                    self.print_timestamp(f"{Fore.CYAN + Style.BRIGHT}[ {index + 1} ]{Style.RESET_ALL}")
                    self.tasks(token=token)
                self.print_timestamp(f"{Fore.WHITE + Style.BRIGHT}[ Diamond ]{Style.RESET_ALL}")
                for index, token in enumerate(tokens):
                    self.print_timestamp(f"{Fore.CYAN + Style.BRIGHT}[ {index + 1} ]{Style.RESET_ALL}")
                    state_diamond = self.state_diamond(token=token)
                    if state_diamond['state'] == 'available':
                        self.complete_diamond(token=token, diamond_number=state_diamond['diamondNumber'], total_reward=state_diamond['settings']['totalReward'])
                    elif state_diamond['state'] in ['unavailable', 'failed', 'completed']:
                        next_at = datetime.fromtimestamp(state_diamond['timings']['nextAt'] / 1000).astimezone()
                        farming_times.append(next_at.timestamp())
                        formatted_next_at = next_at.strftime('%x %X %Z')
                        self.print_timestamp(f"{Fore.YELLOW + Style.BRIGHT}[ Diamond Can Be Complete At {formatted_next_at} ]{Style.RESET_ALL}")
                    else:
                        self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ I Can Not Do Anything When 'state' In State Diamond Is {state_diamond['state']} ]{Style.RESET_ALL}")

                if farming_times:
                    now = datetime.now().astimezone().timestamp()
                    wait_times = [farm_end_time - now for farm_end_time in farming_times if farm_end_time > now]
                    if wait_times:
                        sleep_time = min(wait_times) + 30
                    else:
                        sleep_time = 15 * 60
                else:
                    sleep_time = 15 * 60

                sleep_timestamp = datetime.now().astimezone() + timedelta(seconds=sleep_time)
                timestamp_sleep_time = sleep_timestamp.strftime('%X %Z')
                self.print_timestamp(f"{Fore.CYAN + Style.BRIGHT}[ Restarting At {timestamp_sleep_time} ]{Style.RESET_ALL}")
                sleep(sleep_time)
                self.clear_terminal()
            except Exception as e:
                self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ {str(e)} ]{Style.RESET_ALL}")
                continue

if __name__ == '__main__':
    try:
        init(autoreset=True)
        fintopio = Fintopio()
        fintopio.main()
    except (Exception, requests.ConnectionError, requests.JSONDecodeError) as e:
        fintopio.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ {str(e)} ]{Style.RESET_ALL}")
    except KeyboardInterrupt:
        sys.exit(0)