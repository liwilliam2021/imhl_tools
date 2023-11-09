// npm i puppeteer

const puppeteer = require('puppeteer');
var fs = require('fs');
//const {readFileSync, promises: fsPromises} = require('fs');

const URL = 'https://www.ncbi.nlm.nih.gov/gene/';
const MADELEINE_GENE_FILE = 'madeleine_gene_list.txt';
const GOT_DATA = true;

var count = 0;
var error_count = 0

// initalize the browser URL
async function initBrowser() {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    await page.goto(URL);
    return page;
}


async function get_gene_name(page, gene_number) {
    /* CODE DOESN"T HANDLE GENES THAT ARE NO LONGER ALIVE
    // enter the text value
    await page.evaluate((gene_number) => {document.getElementById('term').value = gene_number}, gene_number);
    // press submit button
    await page.evaluate(() => {document.getElementById('search').click()});
    await page.waitForTimeout(8000);
    */

    // this href code allows you to find hidden genes easily
    await page.evaluate((gene_number) => {window.location.href = 
        `https://www.ncbi.nlm.nih.gov/gene?term=${gene_number}%5Buid%5D&cmd=DetailsSearch`}, gene_number);
    await page.waitForTimeout(2000);
    let nameHTML = null;
    for (let _ = 3; _ < 15; _ ++) {
        try {
            nameHTML =  await page.evaluate(() => {
                const temp = document.getElementById('gene-name').innerHTML;
                return temp;
            });
            return nameHTML.slice(nameHTML.indexOf('>') + 1, nameHTML.indexOf('</span>'));
        } catch(err) {
            page.waitForTimeout(1000);
        }
    }

    await page.evaluate((gene_number) => {window.location.href = 
        `https://www.ncbi.nlm.nih.gov/gene/?term=${gene_number}%5Buid%5D`}, gene_number);
    await page.waitForTimeout(2000);
    for (let _ = 3; _ < 15; _++) {
        try {
            nameHTML =  await page.evaluate(() => {
                const temp = document.getElementById('gene-name').innerHTML;
                return temp;
            });
            return nameHTML.slice(nameHTML.indexOf('>') + 1, nameHTML.indexOf('</span>'));
        } catch(err) {
            page.waitForTimeout(1000);
        }
    }

    console.log(`error: ${gene_number}`);
    error_count += 1;
    await page.screenshot({path: `picture${gene_number}.png`});
    await page.waitForTimeout(10000);
    return "NOT AVAILABLE";
}

async function save_to_file(names) {
    const jsonString = JSON.stringify(names, null, 2);
    fs.writeFile('./gene_names.json', jsonString, err => {
        if (err) {
            console.log('Error writing file', err)
        } else {
            console.log('Successfully wrote file')
        }
    })
}

async function run_gene_name_bot (gene_numbers) {
    const page = await initBrowser();
    names = {};
    total_iter = gene_numbers.length;
    for (const gene_number of gene_numbers) {
        gene_name = await get_gene_name(page, gene_number);
        names[gene_number] = gene_name;
        count += 1;
        console.log(`${count} of ${total_iter} complete (${(count/total_iter * 100).toFixed(2)}%): ${names[gene_number]}`);

        if (count % 100 === 0) {
            save_to_file(names);
        }
    }

    save_to_file(names);

    console.log("LOOK YOU'RE DONE!");
    console.log(`Completed with ${error_count} errors`)
    return names;
}

function check_data_unique(names = null) {
    fetch('gene_names.json')
        .then(response => response.json())
        .then(data => 
            {
                if (!!names){
                gene_name_dictionary = names;
                }
                else {
                    gene_name_dictionary = JSON.parse(data);
                }
                gene_name_list = Object.keys(gene_name_dictionary).map(key => gene_name_dictionary[key]);
                gene_name_set = new Set (gene_name_list);
                console.log(`Number O'Duplicates: ${gene_name_list.length - gene_name_set.length}`);
                return (gene_name_list.length === gene_name_set.length)
        })
        .catch(error => console.log(error));
}

const gene_numbers = fs.readFileSync(MADELEINE_GENE_FILE, 'utf-8').split(/\r?\n/);
if (GOT_DATA) {
    check_data_unique();
}
else {
    const names = run_gene_name_bot(gene_numbers);
    check_data_unique(names);
}
