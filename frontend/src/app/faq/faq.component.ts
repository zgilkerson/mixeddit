import { Component, OnInit, HostListener } from '@angular/core';
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
  headers: NodeListOf<Element>;
  hqMap: Map<Element, HeaderElement> = new Map();

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
    this.headers = document.querySelectorAll('h3, h4');
    for (let index = 0; index < this.headers.length; index++) {
      const he: HeaderElement = {
        id: this.headers[index].id,
        innerText: this.headers[index].innerHTML,
        tag: 'question-level-' + this.headers[index].tagName.toLowerCase(),
        active: false
      };
      this.questions.push(he);
      this.hqMap.set(this.headers[index], he);
    }
  }

  @HostListener('window:scroll', ['$event']) onScrollEvent($event) {
    for (let index = 0; index < this.headers.length; index++) {
      if (this.visibleY(this.headers[index])) {
        this.hqMap.get(this.headers[index]).active = true;
      } else {
        this.hqMap.get(this.headers[index]).active = false;
      }
    }
  }

  visibleY(el: Element) {
    const rect = el.getBoundingClientRect();
    const top = rect.top, height = rect.height;
    if (top <= -height) { return false; }
    return top <= document.documentElement.clientHeight;
  }
}

class HeaderElement {
  id: string;
  innerText: string;
  tag: string;
  active: boolean;
}
