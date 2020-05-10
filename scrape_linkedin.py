import json

from bs4 import BeautifulSoup

data = {}


def scrape_experience(soup):

    def get_paragraph_text(element):
        contents = element.decode_contents().split('\n')[0]
        contents = contents.replace('<br/>', '\n')
        return contents

    def get_position_details(position_card):
        title = position_card.select_one('h3')
        title = title.select_one('span:nth-of-type(2)') if title.select('span') else title
        location = position_card.select_one('.pv-entity__location > span:nth-of-type(2)')
        attachment = position_card.select_one('figure')
        attachment_info = None
        if attachment:
            attachment_info = {
                'title': attachment.select_one('h5').text.strip(),
                'link': 'https://linkedin.com' + position_card.find('a', attrs={'data-control-name': 'treasury_thumbnail_cell'})['href']
            }

        return {
            'title': title.text.strip(),
            'location': location.text.strip() if location else None,
            'details': get_paragraph_text(position_card.select_one('.pv-entity__extra-details > p')),
            'duration': position_card.select_one('.pv-entity__bullet-item-v2').text.strip(),
            'dates': position_card.select_one('.pv-entity__date-range > span:nth-of-type(2)').text.strip(),
            'attachment': attachment_info
        }

    def scrape_position_info_single(position_card):
        return {
            'company': position_card.select_one('.pv-entity__secondary-title').text.strip(),
            'total_duration': position_card.select_one('.pv-entity__bullet-item-v2').text.strip(),
            'positions': [get_position_details(position_card)]
        }

    def scrape_position_info_multiple(position_card):
        top_level_company_info = position_card.select_one('.pv-entity__company-summary-info')
        position_details = [get_position_details(position) for position in position_card.select('.pv-entity__position-group-role-item')]
        return {
            'company': top_level_company_info.select_one('h3 > span:nth-of-type(2)').text.strip(),
            'total_duration': top_level_company_info.select_one('h4 > span:nth-of-type(2)').text.strip(),
            'positions': position_details
        }

    experience = []
    experience_cards = soup.select('.pv-profile-section__card-item-v2')
    for experience_card in experience_cards:
        if experience_card.select_one('ul'):
            experience.append(scrape_position_info_multiple(experience_card))
        else:
            experience.append(scrape_position_info_single(experience_card))
    return experience


def main():
    with open('linkedin_profile.html', 'rb') as profile_html:
        soup = BeautifulSoup(profile_html.read(), 'html.parser')
    data['positions'] = scrape_experience(soup)
    with open('linkedin_profile.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)


if __name__ == '__main__':
    main()
