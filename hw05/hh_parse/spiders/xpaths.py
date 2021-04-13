HH_EMPL_XPATH = {
    "empl_title": "//div[@class='company-header']//span[@class='company-header-title-name']/text()",
    "empl_website": "//div[@class='employer-sidebar']//div[@class='employer-sidebar-content']//a[@class='g-user-content'][@data-qa='sidebar-company-site']/@href",
    "empl_desc": "//div[@class='company-description']//div[@class='g-user-content']//p/text()",
    "empl_sphere": "//div[@class='employer-sidebar']//div[@class='employer-sidebar-content']//p/text()"
}

HH_VAC_XPATH = {
    "title": "//div[@class='vacancy-title']//h1[@class='bloko-header-1'][@data-qa='vacancy-title']/text()",
    "salary": "//p[@class='vacancy-salary']/span/text()",
    "desc": "//div[@class='vacancy-section']/div[@data-qa='vacancy-description']/text()",
    "tag": "//div[@class='bloko-tag-list']//div[contains(@data-qa,'bloko-tag bloko-tag_inline skills-element')]//span[@data-qa='bloko-tag__text']/text()",
    "employer_url": "//div[@class='vacancy-company-wrapper']//a[@class='vacancy-company-name']/@href",

}