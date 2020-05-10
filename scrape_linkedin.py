from bs4 import BeautifulSoup
import pprint as pp

data = {}


def scrape_experience(soup):

    def scrape_position_info_single(experience_card):
        # print(experience_card)
        company_info = experience_card.select_one('.pv-entity__summary-info')
        return {
            'company': company_info.select_one('.pv-entity__secondary-title').text.strip(),
            'positions': [
                {
                    'title': company_info.select_one('h3').text.strip(),
                    'details': experience_card.select_one('.pv-entity__extra-details > p').text
                }
            ]
        }

    def scrape_position_info_multiple(experience_card):
        company_info = experience_card.select_one('.pv-entity__company-summary-info')
        return {
            'company': company_info.select_one('h3 > span:nth-of-type(2)').text.strip(),
            'total_duration': company_info.select_one('h4 > span:nth-of-type(2)').text.strip()
        }

    experience_cards = soup.select('.pv-profile-section__card-item-v2')
    for experience_card in experience_cards:
        if experience_card.select_one('.pv-entity__summary-info'):
            pp.pprint(scrape_position_info_single(experience_card), indent=4)
        else:
            scrape_position_info_multiple(experience_card)


def main():
    with open('linkedin_profile.html', 'rb') as profile_html:
        soup = BeautifulSoup(profile_html.read(), 'html.parser')
    scrape_experience(soup)


if __name__ == '__main__':
    main()