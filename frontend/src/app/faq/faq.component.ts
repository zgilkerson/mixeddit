import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-faq',
  templateUrl: './faq.component.html',
  styleUrls: ['./faq.component.scss']
})
export class FaqComponent implements OnInit {
  private fragment: string;
  _sub;
  questions: HeaderElement[] = [];

  constructor(private route: ActivatedRoute) { }

  ngOnInit() {
    this._sub = this.route.fragment.subscribe((hash: string) => {
      if (hash) {
        const cmp = document.getElementById(hash);
        if (cmp) {
          cmp.scrollIntoView();
        }
      } else {
        window.scrollTo(0, 0);
      }
    });
    const headers = document.querySelectorAll('h3, h4');
    for (let index = 0; index < headers.length; index++) {
      this.questions.push({
        id: headers[index].id,
        innerText: headers[index].innerHTML,
        tag: 'question-link-' + headers[index].tagName.toLowerCase()
      });
    }
  }
}

class HeaderElement {
  id: string;
  innerText: string;
  tag: string;
}
