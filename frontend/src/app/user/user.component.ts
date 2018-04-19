import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { HttpErrorResponse } from '@angular/common/http';

import { SpotifyService } from '../spotify.service';
import { MixedditError } from '../mixeddit-error';

@Component({
  selector: 'app-user',
  templateUrl: './user.component.html',
  styleUrls: ['./user.component.css'],
  providers: [SpotifyService]
})
export class UserComponent implements OnInit {
  mixedditForm: FormGroup;
  mixedditValue: any = {'': ''};

  constructor(private fb: FormBuilder, private spotify: SpotifyService) {
    this.createForm();
  }

  ngOnInit() {}

  onSubmit() {
    this.spotify.putPlaylistReplace(this.mixedditForm.value).subscribe(
      (data) => this.mixedditValue = 'received data',
      (error: MixedditError) => {
        this.mixedditValue = error;
      }
    );
  }

  createForm() {
    this.mixedditForm = this.fb.group({
      subreddit: ['', Validators.required],
      playlist: ['', Validators.required]
    });
  }
}
